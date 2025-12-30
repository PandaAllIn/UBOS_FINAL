export default async function handler(req, res) {
  try {
    // Fetch XML from BNR
    const response = await fetch('https://www.bnr.ro/nbrfxrates.xml');
    const xmlText = await response.text();

    // Parse EUR rate using Regex (Simple & Fast)
    // Looking for: <Rate currency="EUR">4.9765</Rate>
    const match = xmlText.match(/<Rate currency="EUR">([0-9.]+)<\/Rate>/);

    if (match && match[1]) {
      const rate = parseFloat(match[1]);
      res.status(200).json({ currency: 'EUR', rate: rate, date: new Date().toISOString() });
    } else {
      throw new Error('Could not parse EUR rate');
    }
  } catch (error) {
    console.error('BNR Fetch Error:', error);
    // Fallback to recent average if fetch fails
    res.status(200).json({ currency: 'EUR', rate: 4.9765, error: 'Fallback used' });
  }
}
