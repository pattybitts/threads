//imports
//import {default as get_val, set_val, add_to_array, add_to_map} from "./util"

//page utilities
var active_hotkeys = new Map();
var input_focus = false;
var last_page = false;

var full_text = "";
var abs_char_count = 0;

var page_start = 0;
var page_text = "";
var page_wordcount = 0;
var page_mentions = new Map();
var page_quotes = new Map();

//scene data storage (will be saved via form)
var scene_wordcount = 0;
var scene_mentions = new Map();
var scene_quotes = new Map();
var scene_features = [];
var char_events = [];
var scene_end = null;

var known_names = [];
var hot_names = new Map();

init();

function init() {
    $(document).keypress(hotkey);
    $("input").focus(function () {
        input_focus = true;
    });
    $("input").blur(function () {
        input_focus = false;
    });
    $("textarea").focus(function () {
        input_focus = true;
    });
    $("textarea").blur(function () {
        input_focus = false;
    });
    $('#next_page_button').click(next_page);
    $('#add_button').click(add_name);
    $('#summary_button').click(generate_summary);
    $('#event_button').click(character_event);
    $('#mark_button').click(mark_scene);
    $('#diagnostic_button').click(diagnostic);
    $('#translate_button').click(translate_summary);
    $('#save_button').click(save_scene);

    active_hotkeys.set(110, ["next_page", []]); //n
    active_hotkeys.set(97, ["add_name", []]); //a
    active_hotkeys.set(103, ["generate_summary", []]); //g
    active_hotkeys.set(115, ["save_scene", []]); //s
    active_hotkeys.set(99, ["character_event", []]); //c
    active_hotkeys.set(109, ["mark_scene", []]); //m
    active_hotkeys.set(100, ["diagnostic", []]); //d
    active_hotkeys.set(116, ["translate_summary", []]); //t

    $.get(get_val('book_file'), read_text);
    abs_char_count = Number(get_val('position'));
    for (var i = 0; i < 10; i++) {
        hot_names.set(i, ["", 0]);
    }
    if (get_val("save_status") == "") { set_val("save_status", "saved"); }

    $('#page_text').text("Page text will appear here:");
    $('#page_quotes').text("Page quotes will appear here:");
    $('#char_hotkeys').html("<b>Character Hotkeys:</b>");

    //this line. is fricking useful.
    //can use this as a precedent for uploading html text and formatting it in init
    $('#report_text').html($('#report_text').text());

    translate_summary();
}

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

function log(string, clear = false) {
    if (clear) {
        set_val('log_box', "");
    }
    set_val('log_box', get_val('log_box') + "\n" + string);
}

function diagnostic() {
    log("***");
    log("Diagnostic:");
    log("***");
    log("Features Info: ");
    log("Length: " + String(scene_features.length));
    log("Terms:");
    for (let sf of scene_features) {
        log(sf);
    }
    log("Features Box: " + get_val('features_box'));
    log("Features Form: " + get_val('features'));
}

function read_text(data, status) {
    if (status == "success") {
        full_text = data;
    } else {
        full_text = "Unexpected error reading text file";
    }
}

function hotkey(key) {
    //log(key.which);
    if (active_hotkeys.has(key.which) && input_focus == false) {
        func = String(active_hotkeys.get(key.which)[0]);
        args = active_hotkeys.get(key.which)[1];
        window[func](args);
    }
}

function save_page_to_scene() {
    //checking that all previous quotes are assigned
    var checked_quotes = true;
    var all_quotes = document.getElementsByClassName('quote_div');
    for (var i = 0, len = all_quotes.length | 0; i < len; i = i + 1) {
        var quote_div = all_quotes[i];
        if (!quote_div.classList.contains("assigned")) {
            checked_quotes = false;
            break;
        }
    }
    if (!checked_quotes) {
        return false;
    }
    //adding previous page info to scene_arrays
    for (let key of page_mentions.keys()) {
        add_to_map(scene_mentions, key, page_mentions.get(key));
    }
    for (let key of page_quotes.keys()) {
        add_to_map(scene_quotes, key, page_quotes.get(key));
        add_to_array(scene_features, key);
    }
    set_val('features_box', scene_features.join("\n"));
    scene_wordcount += page_wordcount;
    page_start = abs_char_count;
    return true;
}

function next_page() {
    var save_status = get_val('save_status');
    if (save_status == "saved") {
        set_val('save_status', "parsing");
    } else if (save_status == "reviewing") {
        log("ERROR: cannot continue until previous scene is saved");
        return;
    }
    if (!last_page) {
        if (!save_page_to_scene()) {
            log("ERROR: Cannot start until all quotes on previous page are assigned");
            return;
        }
    }

    page_quotes.clear();
    var quotes = [];
    var lines = 0;
    var char_inc = 0;
    var in_quote = false;
    var quote_start = 0;
    while ((quotes.length < 5 && lines < 17) || in_quote) {
        next_char = full_text.charAt(abs_char_count + char_inc++);
        if (next_char == "\n") {
            lines++;
        }
        if (next_char == "\"") {
            if (!in_quote) {
                in_quote = true;
                quote_start = abs_char_count + char_inc;
            } else {
                in_quote = false;
                var quote = full_text.substring(quote_start, abs_char_count + char_inc - 1);
                quote.replace("\n", " ");
                quotes.push(quote);
            }
        }
        if (scene_end !== null && char_inc >= scene_end) {
            break;
        }
    }
    $('#page_quotes').empty();
    for (let q of quotes) {
        var quote_html = "<div onclick='select_quote(this)' class='quote_div'>\"" + String(q) + "\"</div>";
        $('#page_quotes').append(quote_html);
    }
    $(".quote_div:first").addClass('selected');

    page_text = full_text.substr(abs_char_count, char_inc);

    process_page_text();
    update_hotkeys();
    if (!last_page) {
        for (let [key, value] of hot_names.entries()) {
            hot_names.set(key, [value[0], value[1] + 1]);
        }
    }

    abs_char_count += char_inc;
}

function character_event() {
    var char_name = get_val('char_name_box');
    if (char_name == "") {
        log("ERROR: Character Events must have a primary name.");
        return;
    } else {
        add_to_array(known_names, char_name);
        add_to_hot_names(char_name);
    }
    var char_aliases = smart_split(get_val('aliases_box'), "[\\v\\r\\n]+");
    for (ca of char_aliases) {
        add_to_array(known_names, ca);
        add_to_hot_names(ca);
    }
    process_page_text();
    add_to_array(char_events, [
        get_val('char_name_box', true),
        smart_split(get_val('aliases_box', true), "[\\v\\r\\n]+"),
        smart_split(get_val('joins_box', true), "[\\v\\r\\n]+"),
        smart_split(get_val('tags_box', true), "[\\v\\r\\n]+")
    ]);
    log("Submitted Character Event for: " + char_name);
}

function update_hotkeys() {
    var char_hotkey_text = "<b>Character Hotkeys:</b>";
    for (let [key, value] of hot_names.entries()) {
        var name_val = value[0];
        if (name_val != "") {
            active_hotkeys.set(48 + key, ["set_quote", [name_val]]); //48 is the 0 key, 49->1, etc 
            char_hotkey_text += name_val + ": " + key + "<br />";
        }
    }
    $('#char_hotkeys').html(char_hotkey_text);
}

function process_page_text() {
    var html_text = page_text;
    var potential_matches = known_names;
    var potential_name = "";
    var best_matches = [];
    var page_caps = new Map();

    page_mentions.clear();
    page_quotes.clear();

    var page_words = smart_split(page_text, "[\\s-.\"]+");
    page_wordcount = page_words.length;
    if (page_wordcount == 0) {
        return;
    }

    //can maybe be refactored now that i can use break
    for (let p of page_words) {
        if (potential_name != "") {
            potential_name += " " + /^"*(['A-Za-z]*)/.exec(p)[1];
        } else if (/^"*([A-Z].*)/.test(p)) {
            potential_name = /^"*(['A-Za-z]*)/.exec(p)[1];
        }
        if (potential_name != "") {
            //log("pm: " + potential_name);
            potential_name = potential_name.replace("'s", "");
            var pm_reg = new RegExp(potential_name + "(\\s*$|\\s+)");
            potential_matches = potential_matches.filter(pm => pm.search(pm_reg) >= 0);
            if (potential_matches.length > 0) {
                best_matches = potential_matches.filter(pm => pm == potential_name);
            } else {
                if (best_matches.length > 0) {
                    //log("bm: " + best_matches);
                    add_to_map(page_mentions, best_matches[0]);
                    best_matches = [];
                    potential_matches = known_names;
                } else {
                    if (/[\s-."]+(?!$)/.test(potential_name)) { potential_name = smart_split(potential_name, "[\\s-.\"]+")[0]; }
                    add_to_map(page_caps, potential_name);
                    potential_name = "";
                    potential_matches = known_names;
                }
                if (/^"*([A-Z].*)/.test(p)) {
                    potential_name = /^"*(['A-Za-z]*)/.exec(p)[1];
                    potential_name = potential_name.replace("'s", "");
                    pm_reg = new RegExp(potential_name + "(\\s*$|\\s+)");
                    potential_matches = potential_matches.filter(pm => pm.search(pm_reg) >= 0);
                    if (potential_matches.length > 0) {
                        best_matches = potential_matches.filter(pm => pm == potential_name);
                    }
                } else {
                    potential_name = "";
                }
            }
        }
    }
    var name_reg = null;
    var name_rep = "";
    var sorted_pm = new Map([...page_mentions.entries()].sort());
    for (let pm of sorted_pm.keys()) {
        name_reg = new RegExp("(?<!>)(" + pm + ")(?![<\\w])", "g");
        name_rep = "<span class='hgreen'>" + pm + "</span>";
        html_text = html_text.replace(name_reg, name_rep);

        add_to_hot_names(pm);
    }
    var sorted_pc = new Map([...page_caps.entries()].sort());
    for (let pc of sorted_pc.keys()) {
        name_reg = new RegExp("(?<!>)(" + pc + ")(?![\\w])", "g");
        name_rep = "<span class='hyellow'>" + pc + "</span>";
        html_text = html_text.replace(name_reg, name_rep);
    }

    update_hotkeys();

    $('#page_text').empty;
    $('#page_text').html(html_text.trim());
}

function add_to_hot_names(name) {
    var in_hot_names = false;
    for (let value of hot_names.values()) {
        if (value[0] === name) {
            value[1] = 0;
            in_hot_names = true;
            break;
        }
    }
    if (!in_hot_names) {
        var high_val = 0;
        var high_key = null;
        for (let key of hot_names.keys()) {
            if (hot_names.get(key)[0] == "") {
                high_key = key;
                break;
            } else if (hot_names.get(key)[1] > high_val) {
                high_key = key;
                high_val = hot_names.get(key)[1];
            }
        }
        if (high_key != null) {
            hot_names.set(high_key, [name, 0]);
        } else {
            log("ERROR: Too many fresh names, no countermeasure yet");
        }
    }
}

function select_quote(quote) {
    var classes = quote.classList;
    $('.quote_div').removeClass("selected");
    $(quote).addClass("selected");
    if (classes.contains("assigned")) {
        $(quote).removeClass("assigned");
        //this nonsense works for now, but I should extract quote text somewhere/somehow else i think
        //now I have get_val working stably, but i'm scared to touch this
        var quote_text = quote.textContent;
        var quote_reg = new RegExp("\".*\"", "s");
        var quote_matches = quote_text.match(quote_reg);
        if (quote_matches != null) {
            quote.textContent = quote_matches[0];
        }
    }
}

function add_name() {
    //There's a bug here where if the user cancels the prompt, it prevents other hotkeys from functioning
    //ignoring for now
    var alias = prompt("Enter new name:", "").trim();
    if (alias === null) {
        log("ERROR: null prompt - need to refresh for hotkey functionality");
        return;
    }
    if (alias == "") {
        log("No Prompt Entry");
    } else {
        add_to_array(known_names, alias);
        add_to_hot_names(alias);
        process_page_text();
    }
}

function set_quote(args) {
    var all_quotes = document.getElementsByClassName('quote_div');
    var quote_div = null;
    var speaker = args[0];
    for (var i = 0, len = all_quotes.length | 0; i < len; i = i + 1) {
        quote_div = all_quotes[i];
        if (quote_div.classList.contains("selected")) {
            add_to_hot_names(speaker);
            var quote_text = quote_div.textContent;
            add_to_map(page_quotes, speaker, smart_split(quote_text).length);
            quote_div.setAttribute("class", "quote_div assigned");
            quote_div.innerHTML = quote_div.innerHTML + "<br /><br />Assigned: " + speaker;
            if (i + 1 < len) {
                all_quotes[i + 1].setAttribute("class", "quote_div selected");
            }
            break;
        }
    }
}

function smart_split(input_text, separator = "\\s+", flags = "") {
    var input_trimmed = input_text.trim();
    if (input_trimmed == "") {
        return []
    }
    var re = new RegExp(separator + "(?!$)", flags);
    return input_trimmed.split(re);

}

function mark_scene() {
    var next_words = prompt("Enter first words of next scene:", "");
    if (next_words === null) {
        log("ERROR: null prompt - need to refresh for hotkey functionality");
        return;
    }
    if (next_words === "") {
        log("No Prompt Entry");
    } else {
        var endpoint = page_text.indexOf(next_words);
        if (endpoint >= 0) {
            scene_end = endpoint;
            abs_char_count = page_start;
            last_page = true;
            next_page();
            set_val('save_status', "reviewing");
        }
    }
}

function generate_summary() {
    log("Generating Summary");
    //checking form fields
    var checked_fields = true;
    checked_fields = get_val('chapter_box') != "" & checked_fields;
    checked_fields = get_val('primary_box') != "" & checked_fields;
    checked_fields = get_val('locations_box') != "" & checked_fields;
    checked_fields = get_val('description_box') != "" & checked_fields;
    if (!checked_fields) {
        log("ERROR: Scene fields empty");
        return;
    }
    //checking and updating last page
    if (!save_page_to_scene()) {
        log("ERROR: Quotes unassigned");
        return;
    }

    //transferring data to gen_form
    set_val('position', page_start);
    set_val('chapter', get_val('chapter_box'));
    set_val('primary', get_val('primary_box'));
    set_val('locations', get_val('locations_box'));
    set_val('description', get_val('description_box'));
    set_val('features', get_val('features_box'));
    set_val('wordcount', scene_wordcount);
    var sm_string = "";
    for (let [key, value] of scene_mentions.entries()) {
        sm_string = sm_string + key + "," + String(value) + "\n";
    }
    sm_string = sm_string.trim();
    set_val('mentions', sm_string);
    var sq_string = "";
    for (let [key, value] of scene_quotes.entries()) {
        sq_string = sq_string + key + "," + String(value) + "\n";
    }
    set_val('quotes', sq_string.trim());
    var ce_string = "";
    for (let ce of char_events) {
        ce_string = ce_string + [ce[0], ce[1].join(), ce[2].join(), ce[3].join()].join(";") + "\n";
    }
    ce_string = ce_string.trim();
    set_val('char_events', ce_string);
    var kn_string = "";
    for (let kn of known_names) {
        kn_string = kn_string + kn + "\n";
    }
    kn_string = kn_string.trim();
    set_val('known_names', kn_string);

    set_val('log', get_val('log_box'));
    $("#gen_form").submit();
}

function translate_summary() {
    set_val('log_box', get_val('log'));
    log("Translating summary data back into page");
    abs_char_count = Number(get_val('position'));
    set_val('chapter_box', get_val('chapter'));
    set_val('primary_box', get_val('primary'));
    set_val('locations_box', get_val('locations'));
    set_val('description_box', get_val('description'));
    set_val('features_box', get_val('features'));
    scene_wordcount = Number(get_val('wordcount'));
    scene_mentions.clear;
    var sm_strings = smart_split(get_val('mentions'), "[\\v\\r\\n]+");
    for (let sm of sm_strings) {
        var sm_fields = sm.split(",");
        add_to_map(scene_mentions, sm_fields[0], sm_fields[1]);
    }
    scene_quotes.clear;
    var sq_strings = smart_split(get_val('quotes'), "[\\v\\r\\n]+");
    for (let sq of sq_strings) {
        var sq_fields = sq.split(",");
        add_to_map(scene_quotes, sq_fields[0], sq_fields[1]);
    }
    char_events.clear;
    var ce_strings = smart_split(get_val('char_events'), "[\\v\\r\\n]+");
    for (let ce of ce_strings) {
        var ce_fields = ce.split(";");
        var ce_name = ce_fields[0];
        var ce_aliases = ce_fields[1].split(",");
        var ce_joins = ce_fields[2].split(",");
        var ce_tags = ce_fields[3].split(",");
        add_to_array(char_events, [ce_name, ce_aliases, ce_joins, ce_tags]);
    }
    scene_features = smart_split(get_val('features'), "[\\v\\r\\n]+");
    known_names = smart_split(get_val('known_names'), "[\\v\\r\\n]+");
}

function save_scene() {
    if (get_val('save_status') != "reviewing") {
        log("ERROR: cannot save until scene is parsed and reviewed!");
        return;
    }
    if (confirm("Are you sure you are ready to upload scene data?")) {
        log("Saving Scene Data to Database!");
        set_val('save_status', 'saved');
        generate_summary();
    }
}