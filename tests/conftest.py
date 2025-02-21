import pytest
from fad.models import Elemento


@pytest.fixture()
def element():

    element_input = Elemento(fck='C30',
                       descricao="Barras retas pi dobradas com D>25",
                       bitolas=25,
                       bitolai=25,
                       bw =37,
                       bf= 333.5,
                       h=200,
                       hf=20,
                       i=10,
                       s=10,
                       bitolainf=25,
                       bitolasup=25,
                       qdntsup=3,
                       qndtinf=16)


    return element_input