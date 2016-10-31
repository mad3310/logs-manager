from abc import abstractmethod


class AbstractOpers(object):

    @abstractmethod
    def create(self):
        raise NotImplementedError, "Cannot call abstract method"

    @abstractmethod
    def start(self):
        raise NotImplementedError, "Cannot call abstract method"

    @abstractmethod
    def stop(self):
        raise NotImplementedError, "Cannot call abstract method"

    @abstractmethod
    def restart(self):
        raise NotImplementedError, "Cannot call abstract method"
