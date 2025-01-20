# (currently unused)

class HTTPStatusCode:
    ## I had to append "code_" to the names of these status codes because some
    ## have the same name as Python keywords
    code_continue: int = 100
    code_switching_protocols: int = 101
    code_ok: int = 200
    code_created: int = 201
    code_accepted: int = 202
    code_non_authoritative_information: 203
    code_no_content: int = 204
    code_reset_content: int = 205
    code_partial_content: int = 206
    ## Why do these two responses have the same code?
    code_multiple_choices: int = 300
    code_ambiguous: int = 300
    ## Dude...
    code_moved_permanently: int = 301
    code_moved: int = 301
    ## These don't even mean the same thing
    code_found: int = 302
    code_redirected: int = 302
    code_see_other: int = 303
    code_redirected_method: int = 303
    code_not_modified: int = 304
    code_use_proxy: int = 305
    code_unused: int = 306
    code_temporary_redirect: int = 307
    code_redirect_keep_very: int = 307
    code_bad_request: int = 400
    code_unauthorized: int = 401
    ## You can't make payments on any FirstCash website, nor can you purchase things.
    code_payment_required: int = 402
    code_forbidden: int = 403
    code_not_found: int = 404
    code_method_not_allowed: int = 405
    code_not_acceptable: int = 406
    code_proxy_authentication_required: int = 407
    code_request_timeout: int = 408
    code_conflict: int = 409
    code_gone: int = 410
    code_length_required: int = 411
    code_precondition_failed: int = 412
    code_request_entity_too_large: int = 413
    code_uri_too_long: int = 414
    code_unsupported_media_type: int = 415
    code_requested_range_not_satisfiable: int = 416
