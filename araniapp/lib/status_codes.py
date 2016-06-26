# -*- coding: utf-8 -*-

__INFO__ = {
    100: "Continue",
    101: "Switching Protocols",
    102: "Processing (WebDAV; RFC 2518)"
}

__SUCCESS__ = {
    200: "Ok",
    201: "Created",
    202: "Accepted",
    203: "Non-Authoritative Information (since HTTP/1.1)",
    204: "No Content",
    206: "Partial Content",
    205: "Reset Content",
    207: "Multi-Status (WebDAV; RFC 4918)",
    208: "Already Reported (WebDAV; RFC 5842)",
    226: "IM Used (RFC 3229)"
}

__REDIRECTION__ = {
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    303: "See Other (since HTTP/1.1)",
    304: "Not Modified",
    305: "Use Proxy (since HTTP/1.1)",
    307: "Temporary Redirect (since HTTP/1.1)",
    308: "Permanent Redirect (approved as experimental"
}

__CLIENT_ERROR__ = {
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Requeired",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Timeout",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Request Entity Too Large",
    414: "Request-URI Too Long",
    415: "Unsupported Media Type",
    416: "Requested Range Not Satisfiable",
    417: "Excpetation Failed",
    418: "I'm a teapot (RFC 2324)",
    419: "Authentication Timeout (not in RFC 2616)",
    420: "Method Failure (Spring Framework)",
    422: "Unprocessable Entity (WebDAV; RFC 4918)",
    423: "Locked (WebDAV; RFC 4918)",
    424: "Failed Dependency (WebDAV; RFC 4918) or Method Failure",
    425: " Unordered Collection (Internet draft)",
    426: "Upgrade Required (RFC 2817)",
    428: " Precondition Required (RFC 6585)",
    429: "Too Many Requests (RFC 6585)",
    431: " Request Header Fields Too Large (RFC 6585)",
    440: "Login Timeout (Microsoft)",
    444: "No Response (Nginx)",
    449: "Retry With (Microsoft)",
    450: "Blocked by Windows Parental Controls (Microsoft)",
    451: " Unavailable For Legal Reasons (Internet draft) or (Redirect Microsoft)",
    494: " Request Header Too Large (Nginx)",
    495: "Cert Error (Nginx)",
    496: "No Cert (Nginx)",
    497: " HTTP to HTTPS (Nginx)",
    499: "Client Closed Request (Nginx)"
}

__SERVER_ERROR__ = {
    500: "Internal Server Error",
    501: "No Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    505: "HTTP Version Not Supported",
    506: "Variant Also Negotiates (RFC 2295)",
    507: "Insufficient Storage (WebDAV; RFC 4918)",
    508: "Loop Detected (WebDAV; RFC 5842)",
    509: "Bandwidth Limit Exceeded (Apache bw/limited extension)",
    510: "Not Extended (RFC 2774)",
    511: "Network Authentication Required (RFC 6585)",
    520: "Origin Error (Cloudflare)",
    522: "Connection timed out",
    523: "Proxy Declined Request (Cloudflare)",
    524: "A timeout occurred (Cloudflare)",
    598: " Network read timeout error (Unknown)",
    599: "Network connect timeout error (Unknown)"
}


STATUS_INFO = __INFO__.keys()
STATUS_SUCCESS = __SUCCESS__.keys()
STATUS_REDIRECTION = __REDIRECTION__.keys()
STATUS_CLIENT_ERROR = __CLIENT_ERROR__.keys()
STATUS_SERVER_ERROR = __SERVER_ERROR__.keys()
