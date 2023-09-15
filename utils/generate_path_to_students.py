from .three_years_ago_start_date import past_three_years

def path_to_students()->str:
    """function adds a start date set to three years before today"""
    start_date = past_three_years()
    return f"/stagiaires/traineeContract_listing_trainer.asp?startDate={start_date}"