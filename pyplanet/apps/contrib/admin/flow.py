"""
Game Flow Admin methods and functions.
"""
from pyplanet.contrib.command import Command


class FlowAdmin:
	def __init__(self, app):
		"""
		:param app: App instance.
		:type app: pyplanet.apps.contrib.admin.app.Admin
		"""
		self.app = app
		self.instance = app.instance

	async def on_start(self):
		await self.instance.permission_manager.register('end_round', 'Force ending a round (warmup, race or custom)', app=self.app, min_level=2)
		await self.instance.permission_manager.register('player_points', 'Change the player points', app=self.app, min_level=2)
		await self.instance.permission_manager.register('team_points', 'Change the team points', app=self.app, min_level=2)
		await self.instance.permission_manager.register('points_repartition', 'Change the points repartition', app=self.app, min_level=2)

		# Trackmania specific:
		if self.instance.game.game == 'tm' or self.instance.game.game == 'tmnext':
			await self.instance.command_manager.register(
				Command(command='endround', target=self.end_round, perms='admin:end_round', admin=True,
						description='Ends the current round of play.'),
				Command(command='endwuround', target=self.end_wu_round, perms='admin:end_round', admin=True,
						description='Ends the current warm-up round of play.'),
				Command(command='endwu', target=self.end_wu, perms='admin:end_round', admin=True,
						description='Ends the complete warm-up on this map.'),
				Command(command='pointsrepartition', aliases=['pointsrep'], target=self.set_point_repartition,
						perms='admin:points_repartition', admin=True, description='Alters the points repartitioning.')
					.add_param('repartition', nargs='*', type=str, required=True, help='Repartition, comma or space separated.'),
				Command(command='playerpoints', aliases=['playerpoints'], target=self.set_player_points,
						perms='admin:player_points', admin=True, description='Alters the Players Points for Round, Map, Match.'),
				Command(command='teampoints', aliases=['teampoints'], target=self.set_team_points,
						perms='admin:team_points', admin=True, description='Alters the Teams Points for Round, Map, Match.')
				)

		# Shootmania specific.
		if self.instance.game.game == 'sm':
			pass

	async def end_round(self, player, data, **kwargs):
		await self.instance.gbx.multicall(
			self.instance.gbx('Trackmania.ForceEndRound', encode_json=False, response_id=False),
			self.instance.chat('$ff0Admin $fff{}$z$s$ff0 has forced the current round to end.'.format(player.nickname))
		)

	async def end_wu_round(self, player, data, **kwargs):
		await self.instance.gbx.multicall(
			self.instance.gbx('Trackmania.WarmUp.ForceStopRound', encode_json=False, response_id=False),
			self.instance.chat('$ff0Admin $fff{}$z$s$ff0 has forced the current round to end.'.format(player.nickname))
		)

	async def end_wu(self, player, data, **kwargs):
		await self.instance.gbx.multicall(
			self.instance.gbx('Trackmania.WarmUp.ForceStop', encode_json=False, response_id=False),
			self.instance.chat('$ff0Admin $fff{}$z$s$ff0 has forced the WarmUp to an end.'.format(player.nickname))
		)

	async def set_point_repartition(self, player, data, **kwargs):
		partition = data.repartition

		if len(partition) == 1:
			partition = str(partition[0]).split(',')
		partition = [str(p).strip() for p in partition]

		await self.instance.gbx.multicall(
			self.instance.gbx('Trackmania.SetPointsRepartition', *partition, encode_json=False, response_id=False),
			self.instance.chat('$ff0Admin $fff{}$z$s$ff0 has changed the points repartition to: {}.'.format(
				player.nickname, ','.join(partition))
			)
		)
		
	async def set_player_points(self, player, data, **kwargs):
		
		#login, 'RoundPoints', 'Mappoints', 'Matchpoints' for Sending/Updating PlayerPoints
		#Login is for example q2-lckjXSxai11x2CgX5ew so it needs to be 
		await self.instance.gbx.multicall(
			self.instance.gbx('Trackmania.SetPlayerPoints', 'q2-lckjXSxai11x2CgX5ew', '10', '10', '10', encode_json=False, response_id=False),
			self.instance.chat('$ff0Admin $fff{}$z$s$ff0 has changed Player Points for')
			)
			
	async def set_team_points(self, player, data, **kwargs):
		
		#TeamId, 'RoundPoints', 'Mappoints', 'Matchpoints' for Sending/Updating TeamPoints
		#TeamId = 0 (Blue) or 1 (Red)
		await self.instance.gbx.multicall(
			self.instance.gbx('Trackmania.SetTeamPoints', '1', '1', '1', '1', encode_json=False, response_id=False),
			self.instance.chat('$ff0Admin $fff{}$z$s$ff0 has changed Player Points for')
			)
