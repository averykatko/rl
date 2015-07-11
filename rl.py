#!/usr/bin/env python3
import random, heapq, curses
from enum import Enum

class State:
	"""docstring for State"""
	def __init__(self):
		pass

class Cell:
	"""docstring for Cell"""
	def __init__(self, room, x, y, terrain):
		self.room = room
		self.x = x
		self.y = y
		self.terrain = terrain
		self.items = []

class Level:
	"""docstring for Level"""
	def __init__(self, prevLevel=None):
		pass
		# TODO: level generation

class Entity:
	pass

class Item(Entity):
	def __init__(self, location=None):
		self.location = location # either a mob or a cell
		self.cursed = False
	def reaction_drop(self, mob, state):
		mob.location.items.append(self)
		self.location = mob.location

class Potion(Item):
	def reaction_quaff(self, mob, state):
		return

class ItemNotInInventoryError(Exception):
	def __init__(self, item, mob, message=None):
		self.item = item
		self.mob = mob
		self.message = message
	def __str__(self):
		s = "item " + repr(self.item) + " not in inventory of " + repr(self.mob)
		if self.message is not None:
			s += "; " + message
		return s

def inventory_action(method):
	"""
	decorator for actions on items in a mob's inventory
	raises ItemNotInInventoryError if the item is not in the mob's inventory
	"""
	def new_method(self, item, *args):
		if item not in self.inventory:
			raise ItemNotInInventoryError(item, self)
		return method(self, item, *args)
	return new_method

class Mob(Entity):
	"""docstring for Mob"""
	class Status:
		def __init__(self, cell=None, health=0.0, stamina=0.0, mana=0.0):
			self.cell = cell # Cell of Room where the Mob is
			self.health = health
			self.stamina = stamina
			self.mana = mana
			self.on_fire = False
			self.poisoned = False
			self.paralyzed = False
			self.frozen = False
			self.asleep = False
			self.arms_bound = False
			self.mouth_bound = False
	def __init__(self, location):
		self.status = Mob.Status()
		self.inventory = set()
		self.location = location # a cell

	def action_wait(self, state):
		pass
	@inventory_action
	def action_drop(self, item, state):
		if not item.cursed:
			self.inventory.remove(item)
			item.reaction_drop(self, state)
		else:
			pass
	@inventory_action
	def action_throw(self, item, target, state):
		if not item.cursed:
			pass
		else:
			pass
	@inventory_action
	def action_eat(self, item, state):
		if "reaction_eat" in dir(item):
			self.inventory.remove(item)
			item.reaction_eat(self, state)
		else:
			pass
	@inventory_action
	def action_quaff(self, item, state):
		if "reaction_quaff" in dir(item):
			self.inventory.remove(item)
			item.reaction_quaff(self, state)
		else:
			print("you can't quaff that!!!!")
			pass
	def get_droppables(self, state):
		#return [(lambda s: self.action_drop(i,s)) for i in self.inventory if not i.cursed]
		return [i for i in self.inventory if not i.cursed]
	def get_throwables(self, state):
		return [i for i in self.inventory if not i.cursed]
	def get_eatables(self, state):
		#return [(lambda s: self.action_eat(i,s)) for i in self.inventory if reaction_eat in dir(i)]
		return [i for i in self.inventory if reaction_eat in dir(i)]
	def get_quaffables(self, state):
		#return [(lambda s: self.action_quaff(i,s)) for i in self.inventory if reaction_quaff in dir(i)]
		return [i for i in self.inventory if reaction_quaff in dir(i)]
	def get_targets(self, state):
		return []
	def get_actions(self, state):
		"""returns collection of actions the mob can take in the current state"""
		def get_actions_of(action, lstfn, *args):
			lst = lstfn(state)
			return [(lambda s: action(i, *args, s)) for i in lst]
		actions = [self.wait]
		if not (self.status.frozen or self.status.paralyzed or self.status.asleep):
			if not self.status.arms_bound:
				actions += get_actions_of(action_drop, self.get_droppables)
				if not self.status.mouth_bound:
					actions += get_actions_of(self.action_eat, self.get_eatables)
					actions += get_actions_of(self.action_quaff, self.get_quaffables)
		return actions
	def act(self, state):
		"""select an action and perform it, updating game state"""
		self.action_wait(state)

class Player(Mob):
	"""docstring for Player"""
	def act(self):
		# get user input...
		pass


# def main(...cursesargs...):
# 	init curses stuff
# 	init game
# 	gameRunning = True
# 	while gameRunning:
# 		#TODO: main game loop

# if __name__ == "__main__":
# 	curses.wrapper(main)
