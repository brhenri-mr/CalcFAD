
def test_models_integrity(element):
    '''
    Teste da integridade do modelo, se é possivel criar um
    '''

    assert element.b == 333.5
    assert element.hf == 20


def test_model_area_aco(element):
    '''
    Teste dos resultados no modelo
    '''
    TOL = 10**-1

    assert abs(element.asup  - 14.73) < TOL
    assert abs(element.ainf  - 78.45) < TOL


def test_model_segunda_inercia(element):
    TOL = 10**-1
    assert abs(element.inerciaII - 23048019.11) <TOL

def test_model_linhaneutral(element):
    '''
    Teste dos resultados no modelo
    '''
    TOL = 0.1
    assert abs(element.acolaborante - 593) < TOL
    assert abs(element.d0  - 30.60) < TOL
    assert abs(element.am  - 185.48) < TOL
    assert abs(element.x  - 28.42) < TOL
