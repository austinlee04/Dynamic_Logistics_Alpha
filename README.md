# Dynamin_Logistics_Alpha

parcel code = time code(3 digits) + 'P' + 고유번호(7 digits)    -->     000P1000000
hub code = type code(M : main hub, S : sub hub, D : destination) + 지역 번호(2 digits) + 'K' + 고유번호(3 digits)     -->     H00I00

in Enviroment.py :
  self.hub_data = {hub code : [대기열(deque), 허브 최대용량, name, classification time]}   -->   대기열 = [parcel_code, process num]

in Data_manager.py :
  self.route_log = {parcel code : [출발지, 서브허브 1, 메인허브, 서브허브 2, 도착지, 운송비용]}
  self.time_log = {parcel code : [출발시간, 서브허브 1 하차시간, 서브허브 1 상차시간, 메인허브 하차시간, 메인허브 상차시간, 서브허브 2 하차시간, 서브허브 2 상차시간, 도착시간]}
  
