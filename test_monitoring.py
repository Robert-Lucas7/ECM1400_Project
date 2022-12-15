from monitoring import get_monitoring_sites_and_species, get_most_recent_data_from_API_data, get_sites_currently_monitoring_pollutant
import pytest

def test_get_monitoring_sites_and_species():
    data = get_monitoring_sites_and_species()
    assert type(data) == dict

def test_get_most_recent_data_from_API_data():
    assert type(get_most_recent_data_from_API_data('MY1', 'PM10')) == dict

def test_get_sires_currently_monitoring_pollutant():
    sites_and_pollutants = get_monitoring_sites_and_species()
    assert len(get_sites_currently_monitoring_pollutant(sites_and_pollutants, "NO2")) > 0