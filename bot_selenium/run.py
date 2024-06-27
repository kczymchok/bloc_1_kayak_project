from booking.booking import Booking

#add teardown=True in booking() argument to close the window after action

cities = ["Aigues-Mortes","Bormes-les-Mimosas","Gorges du Verdon","Mont Saint Michel", "Saint Malo", "Bayeux", "Le Havre", "Rouen", "Paris", "Amiens", "Lille", "Strasbourg", "Colmar", "Eguisheim", "Besancon", "Dijon", "Annecy", "Grenoble", "Lyon", "Cassis", "Marseille", "Aix en Provence", "Avignon", "Uzes", "Nimes", "Collioure", "Carcassonne", "Ariege", "Toulouse", "Montauban", "Biarritz", "Bayonne", "La Rochelle"]

all_results = []

try:
    for city in cities:
        with Booking() as bot:
            bot.land_first_page()
            bot.close_signin_booking()
            bot.select_city(city)
            bot.select_date(check_in_date='2024-07-20', check_out_date='2024-07-28')
            bot.select_number_occupancy(3)
            bot.click_search()
            bot.apply_filtration()
            bot.refresh()  # a workaround for the bot to pull the data properly
            bot.report_resutls()

except Exception as e:
    if 'in PATH' in str(e):
        print('There is a problem running this program from the CLI')
    else:
        raise

print("All data processing completed.")




