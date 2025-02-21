# Objetivo

Simples fatigue calculator for bridge slab or rectangular beam. The project aims to verify the additional gradient of tension of the reinforcement bar induced by moment. To ensure the simplice, The calculator were made with a GUI 

## Instalation
To install the project, install all the dependency on `pyproject.toml` and install the project:

```
python instalar.py build
```

# Glossary


## Loads
 - M+: Maximum lived moment (already weighted) applied to element 
 - M-: Minimum  lived moment (already weighted) applied to element
 - Mg: Standard's moment

## Rebar Geometry disposition 

- Ainf: Inferior rebar quantity
- Asup: Superior rebar quantity
- i: Minimum distance between the rebars geometric center and the sections botton
- s: Minimum distance between the rebars geometric center and the sections top


## Section properties

- bw: Inferior section width (if it's retangular, bf and bw is equal)
- bf: Superior section width (if it's retangular, bf and bw is equal)
- h: Section height
- hf: Slab thickness 


## Normas 

- [x] NRB 6118:2023 - Anexo 23

## Recomendações

- [x] Pontes de Concreto Armado, MARCHETII (2008)

# Pacotes

## models

The element of fatigue class

### Element

Class of concret element that gonna be verified

## utils

The auxiliar function needed to plot and calculs for fatigue


