from config.models import IceCashEndpoint


# For Third Party Insurance


def ThirdPartyQoute():
    value = IceCashEndpoint.objects.filter(api_name='3RDPARTYQUOTE', active_status=True).values('api_endpoint')
    return value


def ThirdPartyUpdate():
    value = IceCashEndpoint.objects.filter(api_name='3RDPARTYUPDATE', active_status=True).values('api_endpoint')
    return value


def ThirdPartyPolicy():
    value = IceCashEndpoint.objects.filter(api_name='3RDPARTYPOLICY', active_status=True).values('api_endpoint')
    return value


# For Licensing


def LicensingQoute():
    value = IceCashEndpoint.objects.filter(api_name='LICENSINGQUOTE', active_status=True).values('api_endpoint')
    return value


def LicensingUpdate():
    value = IceCashEndpoint.objects.filter(api_name='LICENSINGUPDATE', active_status=True).values('api_endpoint')
    return value


def LicensingPolicy():
    value = IceCashEndpoint.objects.filter(api_name='LICENSINGPOLICY', active_status=True).values('api_endpoint')
    return value


# For Insurance, Zinara, Radio


def CombinedQoute():
    value = IceCashEndpoint.objects.filter(api_name='COMBINEDQUOTE', active_status=True).values('api_endpoint')
    return value


def CombinedUpdate():
    value = IceCashEndpoint.objects.filter(api_name='COMBINEDUPDATE', active_status=True).values('api_endpoint')
    return value


def CombinedPolicy():
    value = IceCashEndpoint.objects.filter(api_name='COMBINEDPOLICY', active_status=True).values('api_endpoint')
    return value


def ComprehensivePolicy():
    value = IceCashEndpoint.objects.filter(api_name='COMPREHENSIVEQUOTE', active_status=True).values('api_endpoint')
    return value


def REVERSAL():
    value = IceCashEndpoint.objects.filter(api_name='REVERSAL', active_status=True).values('api_endpoint')
    return value