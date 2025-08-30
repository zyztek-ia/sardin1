from backend.app import db
from backend.app.models.vessel import Vessel

class VesselService:
    @staticmethod
    def get_all_vessels():
        """Returns all vessels."""
        return Vessel.query.all()

    @staticmethod
    def get_vessel_by_id(vessel_id):
        """Returns a single vessel by its ID."""
        return Vessel.query.get(vessel_id)

    @staticmethod
    def create_vessel(data, owner_id=None):
        """
        Creates a new vessel.
        'data' is a dictionary containing vessel information.
        """
        mmsi = data.get('mmsi')
        name = data.get('name')

        if not mmsi or not name:
            return None, "MMSI and name are required."

        if Vessel.query.filter_by(mmsi=mmsi).first():
            return None, "A vessel with this MMSI already exists."

        new_vessel = Vessel(
            mmsi=mmsi,
            name=name,
            vessel_type=data.get('vessel_type'),
            length_m=data.get('length_m'),
            beam_m=data.get('beam_m'),
            owner_id=owner_id
        )

        db.session.add(new_vessel)
        db.session.commit()

        return new_vessel, "Vessel created successfully."

    @staticmethod
    def update_vessel(vessel_id, data):
        """Updates an existing vessel."""
        vessel = VesselService.get_vessel_by_id(vessel_id)
        if not vessel:
            return None, "Vessel not found."

        vessel.name = data.get('name', vessel.name)
        vessel.vessel_type = data.get('vessel_type', vessel.vessel_type)
        vessel.length_m = data.get('length_m', vessel.length_m)
        vessel.beam_m = data.get('beam_m', vessel.beam_m)

        db.session.commit()
        return vessel, "Vessel updated successfully."

    @staticmethod
    def delete_vessel(vessel_id):
        """Deletes a vessel."""
        vessel = VesselService.get_vessel_by_id(vessel_id)
        if not vessel:
            return False, "Vessel not found."

        db.session.delete(vessel)
        db.session.commit()
        return True, "Vessel deleted successfully."
