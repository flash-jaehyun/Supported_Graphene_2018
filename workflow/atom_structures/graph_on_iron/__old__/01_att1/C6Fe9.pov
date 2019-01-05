#include "colors.inc"
#include "finish.inc"

global_settings {assumed_gamma 1 max_trace_level 6}
background {color White}
camera {orthographic
  right -12.84*x up 13.36*y
  direction 1.00*z
  location <0,0,50.00> look_at <0,0,0>}
light_source {<  2.00,   3.00,  40.00> color White
  area_light <0.70, 0, 0>, <0, 0.70, 0>, 3, 3
  adaptive 1 jitter}

#declare simple = finish {phong 0.7}
#declare pale = finish {ambient .5 diffuse .85 roughness .001 specular 0.200 }
#declare intermediate = finish {ambient 0.3 diffuse 0.6 specular 0.10 roughness 0.04 }
#declare vmd = finish {ambient .0 diffuse .65 phong 0.1 phong_size 40. specular 0.500 }
#declare jmol = finish {ambient .2 diffuse .6 specular 1 roughness .001 metallic}
#declare ase2 = finish {ambient 0.05 brilliance 3 diffuse 0.6 metallic specular 0.70 roughness 0.04 reflection 0.15}
#declare ase3 = finish {ambient .15 brilliance 2 diffuse .6 metallic specular 1. roughness .001 reflection .0}
#declare glass = finish {ambient .05 diffuse .3 specular 1. roughness .001}
#declare glass2 = finish {ambient .0 diffuse .3 specular 1. reflection .25 roughness .001}
#declare Rcell = 0.070;
#declare Rbond = 0.100;

#macro atom(LOC, R, COL, TRANS, FIN)
  sphere{LOC, R texture{pigment{color COL transmit TRANS} finish{FIN}}}
#end
#macro constrain(LOC, R, COL, TRANS FIN)
union{torus{R, Rcell rotate 45*z texture{pigment{color COL transmit TRANS} finish{FIN}}}
      torus{R, Rcell rotate -45*z texture{pigment{color COL transmit TRANS} finish{FIN}}}
      translate LOC}
#end

cylinder {< -4.15,  -2.23, -15.00>, <  1.91,  -2.23, -15.00>, Rcell pigment {Black}}
cylinder {< -1.12,   3.02, -15.00>, <  4.94,   3.02, -15.00>, Rcell pigment {Black}}
cylinder {< -1.12,   3.02,   0.00>, <  4.94,   3.02,   0.00>, Rcell pigment {Black}}
cylinder {< -4.15,  -2.23,   0.00>, <  1.91,  -2.23,   0.00>, Rcell pigment {Black}}
cylinder {< -4.15,  -2.23, -15.00>, < -1.12,   3.02, -15.00>, Rcell pigment {Black}}
cylinder {<  1.91,  -2.23, -15.00>, <  4.94,   3.02, -15.00>, Rcell pigment {Black}}
cylinder {<  1.91,  -2.23,   0.00>, <  4.94,   3.02,   0.00>, Rcell pigment {Black}}
cylinder {< -4.15,  -2.23,   0.00>, < -1.12,   3.02,   0.00>, Rcell pigment {Black}}
cylinder {< -4.15,  -2.23, -15.00>, < -4.15,  -2.23,   0.00>, Rcell pigment {Black}}
cylinder {<  1.91,  -2.23, -15.00>, <  1.91,  -2.23,   0.00>, Rcell pigment {Black}}
cylinder {<  4.94,   3.02, -15.00>, <  4.94,   3.02,   0.00>, Rcell pigment {Black}}
cylinder {< -1.12,   3.02, -15.00>, < -1.12,   3.02,   0.00>, Rcell pigment {Black}}
atom(< -4.15,  -2.23,  -8.00>, 0.79, rgb <0.87, 0.40, 0.20>, 0.0, ase3) // #0 
atom(< -2.13,  -2.23,  -8.00>, 0.79, rgb <0.87, 0.40, 0.20>, 0.0, ase3) // #1 
atom(< -0.11,  -2.23,  -8.00>, 0.79, rgb <0.87, 0.40, 0.20>, 0.0, ase3) // #2 
atom(< -3.14,  -0.48,  -8.00>, 0.79, rgb <0.87, 0.40, 0.20>, 0.0, ase3) // #3 
atom(< -1.12,  -0.48,  -8.00>, 0.79, rgb <0.87, 0.40, 0.20>, 0.0, ase3) // #4 
atom(<  0.90,  -0.48,  -8.00>, 0.79, rgb <0.87, 0.40, 0.20>, 0.0, ase3) // #5 
atom(< -2.13,   1.27,  -8.00>, 0.79, rgb <0.87, 0.40, 0.20>, 0.0, ase3) // #6 
atom(< -0.11,   1.27,  -8.00>, 0.79, rgb <0.87, 0.40, 0.20>, 0.0, ase3) // #7 
atom(<  1.91,   1.27,  -8.00>, 0.79, rgb <0.87, 0.40, 0.20>, 0.0, ase3) // #8 
atom(< -4.15,  -2.23,  -7.00>, 0.46, rgb <0.56, 0.56, 0.56>, 0.0, ase3) // #9 
atom(< -3.14,  -0.48,  -7.00>, 0.46, rgb <0.56, 0.56, 0.56>, 0.0, ase3) // #10 
atom(<  1.91,   1.27,  -7.00>, 0.46, rgb <0.56, 0.56, 0.56>, 0.0, ase3) // #11 
atom(< -1.12,  -0.48,  -7.00>, 0.46, rgb <0.56, 0.56, 0.56>, 0.0, ase3) // #12 
atom(< -0.11,   1.27,  -7.00>, 0.46, rgb <0.56, 0.56, 0.56>, 0.0, ase3) // #13 
atom(< -0.11,  -2.23,  -7.00>, 0.46, rgb <0.56, 0.56, 0.56>, 0.0, ase3) // #14 
