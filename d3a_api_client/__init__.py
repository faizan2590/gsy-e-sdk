from abc import ABC, abstractmethod


class APIClientInterface(ABC):
    """
    Interface for D3A API clients, that support different communication protocols.
    This interface defines the common user functionality that these clients should
    support.
    """

    @abstractmethod
    def __init__(self, market_id, client_id, *args, **kwargs):
        """
        On the constructor of the interface, it is obligatory for the user to provide
        the ID of the market that wants to access, and also to provide his client identifier
        so that D3A can authenticate the connected user.
        :param market_id: Identifier of the market to be connected to
        :param client_id: Identifier of the client
        :param kwargs:
        """
        pass

    @abstractmethod
    def register(self, is_blocking):
        """
        Registers the client to a D3A endpoint. According to the client might be part of
        the constructor, to allow the client to automatically register when creating
        the client object.
        :param is_blocking: Controls whether the client should wait for the registration process
        to finish or to not wait and poll manually or get notified by the event callback.
        :return: None
        """
        pass

    @abstractmethod
    def unregister(self, is_blocking):
        """
        Unregisters the connected client from the D3A endpoint.
        :param is_blocking: Controls whether the client should wait for the unregister process
        to finish or to not wait and poll manually or get notified by the event callback.
        :return: None
        """
        pass

