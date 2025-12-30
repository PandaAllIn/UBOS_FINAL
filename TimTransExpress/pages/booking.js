import { useState, useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { Calendar, Users, MapPin, ArrowRight, Check, CreditCard, Phone, Mail, User } from 'lucide-react';

export default function Booking() {
  // State for form fields
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    route: 'budapesta', // default
    date: '',
    time: '08:00',
    passengers: 1,
    children: 0,
    name: '',
    phone: '',
    email: '',
    address: '',
    notes: ''
  });

  // Exchange rate state
  const [exchangeRate, setExchangeRate] = useState(4.9765); // Default fallback
  const [prices] = useState({
    budapesta: 40,
    viena: 65,
    belgrad: 0, // Negotiable
    other: 0    // Custom
  });

  useEffect(() => {
    // Fetch real-time BNR rate
    fetch('/api/bnr-rate')
      .then(res => res.json())
      .then(data => {
        if (data.rate) {
          setExchangeRate(data.rate);
        }
      })
      .catch(err => console.error('Failed to fetch rate:', err));
  }, []);

  // Calculate totals
  let pricePerPerson = prices[formData.route] || 0;
  
  // Custom logic for Adaptive Transport
  let estimatedPrice = 0;
  if (formData.route === 'other') {
     // If distance is entered, calculate: 1.30 EUR/km
     // Note: This is usually per car, not per person, but let's keep it simple or assume per car total
     if (formData.distance) {
        estimatedPrice = parseFloat(formData.distance) * 1.30;
     }
  } else {
     estimatedPrice = pricePerPerson * (formData.passengers + formData.children);
  }
  
  const totalEur = estimatedPrice.toFixed(2);
  const totalRon = (totalEur * exchangeRate).toFixed(2);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handlePassengerChange = (type, operation) => {
    setFormData(prev => {
      const current = prev[type];
      let newVal = operation === 'inc' ? current + 1 : current - 1;
      if (newVal < 0) newVal = 0;
      if (type === 'passengers' && newVal < 1) newVal = 1; // Min 1 adult
      return { ...prev, [type]: newVal };
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Here we would send the data to an API
    alert('Mulțumim! Rezervarea a fost trimisă. Te vom contacta în curând pentru confirmare.');
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans">
      <Head>
        <title>Rezervare | TimTransExpress</title>
      </Head>

      {/* Navigation */}
      <nav className="bg-white shadow-sm sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <Link href="/" className="text-2xl font-black text-blue-900 tracking-tight cursor-pointer">
            TimTransExpress
          </Link>
          <div className="flex gap-4">
             <Link href="/" className="text-gray-600 hover:text-blue-900 font-medium">Acasă</Link>
             <Link href="/services" className="text-gray-600 hover:text-blue-900 font-medium">Servicii</Link>
          </div>
        </div>
      </nav>

      <main className="container mx-auto px-4 py-12">
        <div className="max-w-5xl mx-auto">
          <h1 className="text-3xl md:text-4xl font-bold text-center text-blue-900 mb-2">Rezervă Călătoria Ta</h1>
          <p className="text-center text-gray-500 mb-12">Completează formularul de mai jos pentru a solicita o rezervare.</p>

          <div className="grid md:grid-cols-3 gap-8">
            
            {/* Left Column: Form */}
            <div className="md:col-span-2 space-y-6">
              <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-lg p-6 md:p-8">
                
                {/* Step 1: Trip Details */}
                <div className="mb-8">
                  <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                    <span className="bg-blue-100 text-blue-600 w-8 h-8 rounded-full flex items-center justify-center text-sm">1</span>
                    Detalii Cursă
                  </h2>
                  
                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Destinație</label>
                      <div className="relative">
                        <MapPin className="absolute left-3 top-3 text-gray-400" size={20} />
                        <select 
                          name="route" 
                          value={formData.route} 
                          onChange={handleInputChange}
                          className="w-full pl-10 pr-4 py-3 rounded-lg border border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition appearance-none bg-white"
                        >
                          <option value="budapesta">Timișoara → Budapesta (€40)</option>
                          <option value="viena">Timișoara → Viena (€65)</option>
                          <option value="belgrad">Timișoara → Belgrad (Negociabil)</option>
                          <option value="other">Altă destinație / Adaptiv (€1.30/km)</option>
                        </select>
                      </div>
                      
                      {formData.route === 'other' && (
                        <div className="mt-4 animate-fade-in">
                          <label className="block text-sm font-medium text-gray-700 mb-2">Distanță estimată (km)</label>
                          <div className="relative">
                             <Calculator className="absolute left-3 top-3 text-gray-400" size={20} />
                             <input 
                               type="number" 
                               name="distance"
                               placeholder="Ex: 150"
                               onChange={handleInputChange}
                               className="w-full pl-10 pr-4 py-3 rounded-lg border border-gray-200 focus:border-blue-500 outline-none transition"
                             />
                          </div>
                          <p className="text-xs text-gray-500 mt-1">Preț estimativ: €1.30 / km</p>
                        </div>
                      )}
                    </div>

                    <div>
                       <label className="block text-sm font-medium text-gray-700 mb-2">Data Plecării</label>
                       <div className="relative">
                         <Calendar className="absolute left-3 top-3 text-gray-400" size={20} />
                         <input 
                           type="date" 
                           name="date"
                           value={formData.date}
                           onChange={handleInputChange}
                           required
                           className="w-full pl-10 pr-4 py-3 rounded-lg border border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition"
                         />
                       </div>
                    </div>
                  </div>
                  
                  <div className="mt-6">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Pasageri</label>
                    <div className="flex gap-8 bg-gray-50 p-4 rounded-xl border border-gray-100">
                      <div className="flex-1">
                        <span className="text-sm text-gray-500 block">Adulți</span>
                        <div className="flex items-center gap-3 mt-1">
                          <button type="button" onClick={() => handlePassengerChange('passengers', 'dec')} className="w-8 h-8 rounded-full bg-white border shadow-sm hover:bg-gray-100 font-bold text-gray-600">-</button>
                          <span className="text-xl font-bold w-6 text-center">{formData.passengers}</span>
                          <button type="button" onClick={() => handlePassengerChange('passengers', 'inc')} className="w-8 h-8 rounded-full bg-white border shadow-sm hover:bg-gray-100 font-bold text-blue-600">+</button>
                        </div>
                      </div>
                      <div className="flex-1 border-l border-gray-200 pl-8">
                        <span className="text-sm text-gray-500 block">Copii</span>
                        <div className="flex items-center gap-3 mt-1">
                          <button type="button" onClick={() => handlePassengerChange('children', 'dec')} className="w-8 h-8 rounded-full bg-white border shadow-sm hover:bg-gray-100 font-bold text-gray-600">-</button>
                          <span className="text-xl font-bold w-6 text-center">{formData.children}</span>
                          <button type="button" onClick={() => handlePassengerChange('children', 'inc')} className="w-8 h-8 rounded-full bg-white border shadow-sm hover:bg-gray-100 font-bold text-blue-600">+</button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Step 2: Contact Details */}
                <div className="mb-8 pt-8 border-t border-gray-100">
                  <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                    <span className="bg-blue-100 text-blue-600 w-8 h-8 rounded-full flex items-center justify-center text-sm">2</span>
                    Datele Tale
                  </h2>

                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Nume Complet</label>
                      <div className="relative">
                        <User className="absolute left-3 top-3 text-gray-400" size={20} />
                        <input 
                          type="text" 
                          name="name"
                          placeholder="Ex: Ion Popescu"
                          value={formData.name}
                          onChange={handleInputChange}
                          required
                          className="w-full pl-10 pr-4 py-3 rounded-lg border border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition"
                        />
                      </div>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Telefon (WhatsApp)</label>
                      <div className="relative">
                        <Phone className="absolute left-3 top-3 text-gray-400" size={20} />
                        <input 
                          type="tel" 
                          name="phone"
                          placeholder="07xx xxx xxx"
                          value={formData.phone}
                          onChange={handleInputChange}
                          required
                          className="w-full pl-10 pr-4 py-3 rounded-lg border border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition"
                        />
                      </div>
                    </div>
                  </div>

                  <div className="mt-4">
                     <label className="block text-sm font-medium text-gray-700 mb-2">Adresă Preluare (Timișoara)</label>
                     <input 
                        type="text" 
                        name="address"
                        placeholder="Strada, Număr, Detalii..."
                        value={formData.address}
                        onChange={handleInputChange}
                        required
                        className="w-full px-4 py-3 rounded-lg border border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition"
                      />
                  </div>

                  <div className="mt-4">
                     <label className="block text-sm font-medium text-gray-700 mb-2">Note Speciale (Opțional)</label>
                     <textarea 
                        name="notes"
                        rows="3"
                        placeholder="Ex: Multe bagaje, nevoie de scaun copil, etc."
                        value={formData.notes}
                        onChange={handleInputChange}
                        className="w-full px-4 py-3 rounded-lg border border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition"
                      ></textarea>
                  </div>
                </div>

                <button 
                  type="submit" 
                  className="w-full bg-yellow-500 hover:bg-yellow-400 text-blue-900 font-bold py-4 rounded-xl shadow-lg hover:shadow-xl transition transform hover:-translate-y-1 text-lg flex justify-center items-center gap-2"
                >
                  Confirmă Rezervarea <ArrowRight size={20}/>
                </button>
                <p className="text-center text-xs text-gray-400 mt-4">Nu se percepe plată acum. Vei fi contactat pentru confirmare.</p>

              </form>
            </div>

            {/* Right Column: Summary */}
            <div className="md:col-span-1">
              <div className="bg-white rounded-2xl shadow-lg p-6 sticky top-24">
                <h3 className="text-lg font-bold text-gray-900 mb-6 pb-4 border-b border-gray-100">Sumar Comandă</h3>
                
                <div className="space-y-4 mb-8">
                  <div className="flex justify-between text-gray-600">
                    <span>Destinație</span>
                    <span className="font-semibold text-gray-900 capitalize">{formData.route}</span>
                  </div>
                  <div className="flex justify-between text-gray-600">
                    <span>Pasageri</span>
                    <span className="font-semibold text-gray-900">{formData.passengers + formData.children} pers</span>
                  </div>
                  <div className="flex justify-between text-gray-600">
                    <span>Dată</span>
                    <span className="font-semibold text-gray-900">{formData.date || '-'}</span>
                  </div>
                </div>

                {pricePerPerson > 0 ? (
                  <div className="bg-blue-50 rounded-xl p-4 mb-6">
                    <div className="flex justify-between items-end mb-2">
                      <span className="text-gray-600">Total Euro</span>
                      <span className="text-3xl font-bold text-blue-900">€{totalEur}</span>
                    </div>
                    <div className="flex justify-between items-center text-sm">
                      <span className="text-gray-500">Estimativ RON*</span>
                      <span className="font-bold text-gray-700">{totalRon} RON</span>
                    </div>
                    <div className="mt-3 text-[10px] text-gray-400 leading-tight">
                      *Calculat la cursul BNR estimat de {exchangeRate} RON/EUR. Prețul final în RON se calculează în ziua cursei.
                    </div>
                  </div>
                ) : (
                  <div className="bg-yellow-50 rounded-xl p-4 mb-6 text-center">
                    <span className="text-yellow-700 font-bold block mb-1">Preț la cerere</span>
                    <span className="text-xs text-yellow-600">Te vom contacta cu o ofertă personalizată.</span>
                  </div>
                )}

                <div className="space-y-3">
                  <div className="flex items-center gap-3 text-sm text-gray-500">
                    <Check className="text-green-500" size={16}/> <span>Fără avans obligatoriu</span>
                  </div>
                  <div className="flex items-center gap-3 text-sm text-gray-500">
                    <Check className="text-green-500" size={16}/> <span>Anulare gratuită (24h)</span>
                  </div>
                  <div className="flex items-center gap-3 text-sm text-gray-500">
                    <Check className="text-green-500" size={16}/> <span>Plată cash sau card la șofer</span>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </main>
    </div>
  );
}
