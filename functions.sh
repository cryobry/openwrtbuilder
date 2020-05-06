#!/usr/bin/env bash

extractImage() {

    debug "${FUNCNAME[0]}" "$@"

    local _gz

    [[ $# -lt 1 ]] && echo "extractImage() requires at least one argument" && exit 1

    for _gz in "$@"; do
        [[ ! -f "$_gz" ]] && return 1
        debug "gunzip -qfk $_gz"
        if ! gunzip -qfk "$_gz"; then
            echo "$_gz extraction failed!"
        fi
    done
}
