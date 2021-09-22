from flask_restful import reqparse, Resource
from models.vessel_position import VesselModel
from operator import itemgetter

class VesselPosition(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("latitude", 
                        type=float,
                        required=True, 
                        help="Every vessel position has a latitude!")
    
    parser.add_argument("longitude", 
                        type=float,
                        required=True, 
                        help="Every vessel position has a longitude!")
    
    parser.add_argument("position_time", 
                        type=str,
                        required=True, 
                        help="Every vessel position has a datetime!")
    
    def get(self, vessel_id):
        # get all positions of a specific vessel (vessel_id)

        vessel_history = VesselModel.find_by_vessel_id(vessel_id)
        if vessel_history:
            return {"vessel_history": sorted([vessel.json() for vessel in vessel_history], \
                                              key=itemgetter('position_time')
                                            )}        
        return {"message": "vessel not found"}, 404

    def post(self, vessel_id):

        # add vessel position
        request_data = VesselPosition.parser.parse_args()
        if not -90 <= request_data["latitude"] <= 90:
            raise Exception("Latitude must be in [-90,90]")
        if not -180 <= request_data["longitude"] <= 180:
            raise Exception("Longitude must be in [-180,180]") 
        vessel = VesselModel(vessel_id, **request_data)
        try:
            vessel.save_to_db()
        except:
            return {"message": "Insertion Error! Try again please"}, 500
        
        return {"message":"Vessel position added successfully" ,"vessel": vessel.json()}, 201


class VesselsList(Resource):
    # List all positions of all vessels

    def get(self):
        return {"all_vessels": [vessel.json() for vessel in VesselModel.query.all()]}
