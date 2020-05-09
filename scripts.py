import ret, data_storage, log
from cmd import ValidCommands
from Series import Series
from Character import Character

#eliminate allegiance property and instead add "Darkfriend" tag to shadow allies
if 1:
    series_info = data_storage.load_pickle(data_storage.ACTIVE_FILE)
    new_series_info = Series()
    for c in series_info.characters:
        new_char = Character(c.name, c.print_aliases(), c.gender, c.tier, c.color["r"], c.color["g"], c.color["b"], c.print_tags())
        if c.allegiance == "Shadow":
            new_char.tags.append("Darkfriend")
        new_series_info.add_char(new_char)
    new_series_info.save("wot_0")

