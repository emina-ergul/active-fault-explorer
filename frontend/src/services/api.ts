
const API_URL = 'http://localhost:8000'

export async function getFaultCount() {
  const response = await fetch(`${API_URL}/faults/count`)

  if (!response.ok) {
    throw new Error('failed to fetch fault count')
  }

  return response.json()
}

export async function getEarthquakes() {
  const response = await fetch(`${API_URL}/earthquakes?start_year=2024&end_year=2026&min_magnitude=3.5&limit=2500`)

  if (!response.ok) {
    throw new Error('failed to fetch earthquakes')
  }

  return response.json()
}

export async function getFaults() {
  const response = await fetch(`${API_URL}/faults`)

  if (!response.ok) {
    throw new Error('failed to fetch faults')
  }

  return response.json()
}