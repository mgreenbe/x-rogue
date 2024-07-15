Visibility mask
- as player moves around, corridors, doors, and walls are unmasked permanently.
- room interiors are unmasked in whole or in part depending on whether a room is light or dark.
- entities (monsters and items)
- mapped (walls, doors, corridors)

- visiblity mask (lit rooms, spaces adjacent to player)

mask entities by visibility

visible_entities = entities*is_visibile

where(visible_entities, [visible_entities, mapped])
If there's a visible entity, show the entity.
Otherwise, show what the player has mapped at that location.

allocate for these:
true_map
player_map
entities
is_visible

visible_entities

curmap = np.where(visible_entities, visible_entities, player_map)

No! Floor and items visible in lit, visited rooms even when the player isn't in them. **Player map must indicate lit, visited rooms and items in them.**

state
-----
waiting for (action key, continue, direction, help key)
depth
map
player stats
player map
player position
player inventory
player visibility mask
monsters
objects
message

actions
-------
- prompt for command
- prompt for potion to quaff, scroll to read, weapon to wield, armor to take off/put on, continue, tentative item name, quit confirmation, direction, not a valid item, command to execute multiple times, item-character to identify
- continue
- player move (with or without picking up) or attack
- pick up item
- drop item
- monster move or attack
- wield weapon
- put on armor
- take off armor
- put on ring
- take off ring
- game over
- end program
- advance to next level
- throw item
- run and attack/pick up
- run till adjacent
- repeat last command
- inventory
- inventory single item
- show what's been discovered
- show/set options
- save game
- redraw screen
- repeat last message
- cancel command