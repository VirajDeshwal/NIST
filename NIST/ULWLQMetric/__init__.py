#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import division

from MDmisc import fuckit
from MDmisc.boxer import boxer
from MDmisc.logger import debug
from MDmisc.map_r import map_r
from MDmisc.string import split_r, split
from PMlib.formatConverter import cooNIST2PIL
from SoftPillow import Image
    
from ..fingerprint import NISTf
from ..fingerprint import AnnotationList, Minutia
from ..traditional import RS, US
from ..traditional import needNtype
    
try:
    from ULWLQMetric import ULWLQMetric

    class NISTULWLQMetric( NISTf, ULWLQMetric ):
        """
            Wrapper for the ULWLQMetric module, to be directly integrated in the
            NIST object.
        """
        @property
        def img( self ): 
            return self.get_latent( 'PIL' )
        
        def ULWLQMetric_update_data( self, idc = -1 ):
            """
                Encode the quality of the image, and update the correspondings
                filds in the NIST object.
            """
            idc = self.checkIDC( 9, idc )
            self.data[ 9 ][ idc ].update( super( NISTULWLQMetric, self ).ULWLQMetric_encode( 'EFS' ) )
        
        def get_LQMetric_map( self, idc = -1 ):
            """
                Get the LQMetric map of quality (field 9.308).
                
                :param idc: IDC value.
                :type idc: int
                
                :return: Quality map
                :rtype: str
            """
            return super( NISTULWLQMetric, self ).ULWLQMetric_encode( "EFS" )[ 308 ]
        
        def add_LQMetric_data( self, lst, idc = -1 ):
            """
                Add the ULW LQMetric for each Annotation passed in parameter.
                The LQMetric is evaluated from the quality map stored in the
                NIST object (in the field 9.308). 
            """
            # Add the LQMetric quality 
            qmap = self.get_field( "9.308" )
            
            if qmap != None:
                qmap = map( list, split( RS, qmap ) )
                
                h = self.get_height( idc )
                res = self.get_resolution( idc )
                
                for m in lst:
                    coo = cooNIST2PIL( ( m.x, m.y ), h, res )
                    x, y = map_r( lambda x: int( x / 4 ), coo )
                    try:
                        m.LQM = int( qmap[ y ][ x ] )
                    except:
                        m.LQM = None
                
                newformat = list( lst[ 0 ]._format )
                newformat.append( "LQM" )
                
                lst.set_format( newformat )
            
            return lst
        
        def get_minutiae( self, format = None, idc = -1, **options ):
            """
                Overload of the get_minutiae function to add the LQMetric information.
            """
            lst = super( NISTULWLQMetric, self ).get_minutiae( format = format, idc = idc, **options )
            
            with fuckit:
                lst = self.add_LQMetric_data( lst )
            
            return lst
            
        def get_minutiae_by_LQM( self, criteria, higher = True, format = None, idc = -1, field = None ):
            """
                Filter out the minutiae based on the LQMetric value
            """
            lst = AnnotationList()
            
            minu = self.get_minutiae( format, idc = idc, field = field )
            
            for m in minu:
                if m.LQM >= criteria and higher:
                    lst.append( m )
                
                elif m.LQM <= criteria and not higher:
                    lst.append( m )
            
            return lst
        
        def get_latent_triptych( self, content = "quality", idc = -1 ):
            """
                Get the triptych : latent, annotated latent, quality map (ULW).
            """
            if content == "quality":
                diptych = self.get_latent_diptych( idc )
                
                qmap = super( NISTULWLQMetric, self ).ULWLQMetric_encode( "image" )
                
                qmap = qmap.chroma( ( 0, 0, 0 ) )
                qmap = qmap.transparency( 0.5 )
                qmap = qmap.scale( self.get_resolution( idc ) * 4 / 500.0 )
                
                latentqmap = self.get_latent( 'PIL', idc )
                latentqmap = latentqmap.convert( "RGBA" )
                latentqmap.paste( qmap, ( 0, 0 ), mask = qmap )
                
                new = Image.new( "RGB", ( self.get_width( idc ) * 3, self.get_height( idc ) ), "white" )
                
                new.paste( diptych, ( 0, 0 ) )
                new.paste( latentqmap, ( diptych.size[ 0 ], 0 ) )
                
                return new
            
            else:
                super( NISTULWLQMetric, self ).get_latent_triptych( content, idc )
            
except:
    debug.critical( boxer( "ULWLQMetric module not found", "Have you installed the ULWLQMetric library?" ) )
