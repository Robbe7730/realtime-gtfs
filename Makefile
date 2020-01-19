test:
	venv/bin/python -m pytest --cov=realtime_gtfs --pylint

test_slow:
	venv/bin/python -m pytest --cov=realtime_gtfs --pylint --runslow

test_no_integration:
	venv/bin/python -m pytest --cov=realtime_gtfs --pylint --no-integration
