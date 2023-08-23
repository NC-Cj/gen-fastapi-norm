from abc import ABC, abstractmethod


class ResultConverter(ABC):
    @abstractmethod
    def convert(self,
                result):
        pass


class DictConverter(ResultConverter):
    @classmethod
    def convert(cls,
                result):
        if isinstance(result, list):
            return [item.to_dict() for item in result]

        return result.to_dict()
