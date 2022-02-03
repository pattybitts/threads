function add_to_map(list, term, count = 1) {
    for (let key of list.keys()) {
        if (key == term) {
            list.set(key, list.get(key) + count);
            return;
        }
    }
    list.set(term, count);
}

function add_to_array(list, term) {
    if (!list.includes(term)) {
        list.push(term);
    }
}

function get_val(element, clear = false) {
    var el = $('#' + element);
    if (el.length === 0) {
        log("ERROR: failed to find element id: " + element);
        return null;
    }
    var ret = el.val();
    if (clear) {
        el.val("");
    }
    return ret;
}

function set_val(element, new_val, clear = true) {
    var el = $('#' + element);
    if (el.length === 0) {
        return false;
    }
    if (clear) {
        el.val(String(new_val));
    } else {
        el.val(el.val() + new_val);
    }
    return true;
}