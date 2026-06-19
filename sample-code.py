from hammerapi import HammerAPI

hammer = HammerAPI(max_workers=10)
hammer.add_test("GET", "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
hammer.run(duration_seconds=10)
hammer.generate_report("timed_stress_test.html")