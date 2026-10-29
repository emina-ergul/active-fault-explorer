
const API_URL = 'http://localhost:8000'

export async function getEarthquakes() {
  const response = await fetch(`${API_URL}/earthquakes`)

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