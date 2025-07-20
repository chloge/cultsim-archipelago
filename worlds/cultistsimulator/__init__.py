from worlds.AutoWorld import World, WebWorld
from BaseClasses import MultiWorld, Region
from worlds.generic.Rules import add_rule
from typing import Dict, List, Tuple

from .Items import CSItemClassification, CSItem, item_dict
from .Locations import CSLocationClassification, CSLocation, location_dict

class CultistSimulator(World):
    """
    Cult
    """
    game = "Cultist Simulator"
    topology_present = True
    startid = 2121210000
    item_name_to_id = {item: id for id, item in enumerate(item_dict.keys(), startid)}
    location_name_to_id = {location: id for id, location in enumerate(location_dict.keys(), startid)}

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)

    def create_item(self, item: str) -> CSItem:
        return CSItem(item, item_dict.get(item)[0], self.item_name_to_id[item], self.player)

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        locations: Dict[str] = {name: self.location_name_to_id[name] for name in location_dict.keys()}
        # Capital region, contains everything
        capital_region = Region("Capital", self.player, self.multiworld)
        capital_region.add_locations(locations, CSLocation)
        self.multiworld.regions.append(capital_region)
        menu_region.connect(capital_region)
    
    def create_items(self) -> None:
        # Add all items to the world
        # exclude = [item for item in self.multiworld.precollected_items[self.player]]

        for item in map(self.create_item, item_dict.keys()):
            self.multiworld.itempool.append(item)

        # There is currently no way to end up with more or less items present that the item pool size
        # If for some reason this changes, we will fill the extra spots with funds
        #junk = 0
        #self.multiworld.itempool += [self.create_item("funds") for _ in range(junk)]

    # Note on logic:
    # CS has been proven to be beatable in a standard run without:
        # -Doing expeditions
        # -Having reason
        # -Dreaming
        # -Breaking the law
        # -Reading
        # -Making a cult at all
    # So for an adept player, logic is not required.
    # However, there is an extremely (as in 1-5 possible generations out of all possible with all items) low chance the game will be uncompletable if only using this randomizer standalone.
    # Should the progression end up being too inaccessible or frustrating or if the above cases EVER show up, logic will be added.

