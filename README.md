# CalcFAD — Fatigue Calculator for RC Elements

> Python desktop application for fatigue verification of reinforced concrete 
> beams and bridge slabs, following NBR 6118:2023 (Annex 23).

![Python](https://img.shields.io/badge/Python-3.x-blue)
![PySimpleGUI](https://img.shields.io/badge/GUI-PySimpleGUI-orange)
![License](https://img.shields.io/badge/license-MIT-green)


## Features

- Fatigue verification per NBR 6118:2023 (Annex 23)
- Supports rectangular beams and T-sections (bridge slabs)
- Desktop GUI via PySimpleGUI
- Modular architecture (models + utils)
- Unit tests included


## Installation
```bash
git clone https://github.com/brhenri-mr/CalcFAD
cd CalcFAD
python instalar.py build
```

## Input Parameters

| Parameter | Description |
|-----------|-------------|
| M+ / M-   | Max/min live moments (weighted) |
| Mg        | Standard moment |
| Ainf / Asup | Inferior/superior rebar area |
| bw / bf   | Section widths |
| h / hf    | Section height / slab thickness |


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


