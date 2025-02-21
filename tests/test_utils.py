from fad.utils import tensaoArmadura



def test_tensao_aco(element):

    TOL = 0.1


    momento_max_comb = 130373.84 + 0.5*295489.9166
    momento_min_comb = 130373.84 + 0.5*-135438.52
    tensoes = [element.tensaoConcreto(momento) for momento in [momento_max_comb, momento_min_comb]]

    assert abs(tensoes[0] - 0.34 ) < TOL
    assert abs(tensoes[1] - 0.08 ) < TOL

    deltatensao = [tensaoArmadura(sigmac=tensoes[0], 
                                          sigmacmin=tensoes[1], 
                                          d_max=element.d_posi if momento_max_comb>0 else element.d_neg, 
                                          d_min=element.d_posi if momento_min_comb>0 else element.d_neg,
                                          dlinha_min= element.dlinha_posi if momento_min_comb>0 else element.dlinha_neg,
                                          dlinha_max=element.dlinha_posi if momento_max_comb>0 else element.dlinha_neg, 
                                          x_max= element.x_posi if momento_max_comb>0 else element.x_neg, 
                                          x_min=element.x_posi if momento_min_comb>0 else element.x_neg,
                                          ae=element.ae, 
                                          TYPE=tipo) for tipo in ['Inferior', 'Superior']]

    assert abs(deltatensao[0] - 151.05) < TOL 
    assert abs(deltatensao[1] - 17.22) <TOL 











