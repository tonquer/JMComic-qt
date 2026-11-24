import curl_cffi.requests.exceptions as exceptions

from tools.status import Status


def _ClassifyTlsOrReset(err: Exception, defaultStatus: int) -> int:
    msg = str(err)
    if "Connection was reset" in msg:
        return Status.ResetErr
    if "ECH_REJECTED" in msg:
        return Status.EchError
    if "TLSV1_ALERT_UNRECOGNIZED_NAME" in msg:
        return Status.SNIError
    return defaultStatus


def ClassifyRequestError(err: Exception, isDownload: bool = False) -> int:
    """Map a curl_cffi / network exception to the project's Status code."""
    if isinstance(err, exceptions.DNSError):
        return Status.DnsError
    if isinstance(err, exceptions.Timeout):
        return _ClassifyTlsOrReset(err, Status.TimeOut)
    if isinstance(err, exceptions.SSLError):
        return _ClassifyTlsOrReset(err, Status.NetError)
    if isinstance(err, exceptions.ConnectionError):
        return Status.ConnectErr
    if isDownload and isinstance(err, exceptions.RequestException):
        if "timed out" in str(err):
            return Status.TimeOut
        return Status.ConnectErr
    return Status.NetError
