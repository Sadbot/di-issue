from dependency_injector import containers, providers

from ports import Ports


class Container(containers.DeclarativeContainer):
    test_ports = providers.Factory(Ports)
