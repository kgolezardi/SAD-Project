class AuctionFinishedError(Exception):
    pass


class AuctionNotFinishedError(Exception):
    pass


class PriceValidationError(Exception):
    pass


class UserAccessError(Exception):
    pass


class LowCreditError(Exception):
    pass


class AuctionReceivedError(Exception):
    pass


class AuctionFinalizedError(Exception):
    pass
