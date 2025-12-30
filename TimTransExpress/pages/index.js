import Head from 'next/head';
import Link from 'next/link';
import { Phone, MapPin, Clock, Shield, CheckCircle, Car, Users, Calculator } from 'lucide-react';

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col font-sans bg-slate-50">
      <Head>
        <title>TimTransExpress | Transport Aeroport Timișoara - Budapesta - Viena</title>
        <meta name="description" content="Transport zilnic rapid și confortabil din Timișoara către Aeroport Budapesta (€40) și Viena (€65). Mazda CX-7 și Microbuz. Rezervă acum!" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      {/* Navigation */}
      <nav className="bg-white shadow-md sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <div className="text-2xl font-black text-blue-900 tracking-tight">TimTransExpress</div>
          <div className="flex items-center gap-4">
            <a href="tel:+40700000000" className="hidden md:flex bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-full font-bold transition items-center gap-2 shadow-lg">
              <Phone size={18} />
              +40 700 000 000
            </a>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <header className="bg-gradient-to-br from-blue-900 via-blue-800 to-blue-900 text-white py-24 relative overflow-hidden">
        <div className="absolute inset-0 opacity-10 bg-[url('https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?q=80&w=2070&auto=format&fit=crop')] bg-center bg-cover"></div>
        <div className="container mx-auto px-6 text-center relative z-10">
          <h1 className="text-4xl md:text-7xl font-extrabold mb-6 leading-tight">
            Transport Aeroport <br/><span className="text-yellow-400">Rapid & Confortabil</span>
          </h1>
          <p className="text-xl md:text-2xl text-blue-100 mb-10 max-w-3xl mx-auto font-light">
            Legătura ta directă din Timișoara către aeroporturile din <span className="font-bold text-white">Budapesta</span> și <span className="font-bold text-white">Viena</span>.
          </p>
          <div className="flex flex-col md:flex-row justify-center gap-4">
            <Link href="/booking" className="bg-yellow-500 hover:bg-yellow-400 text-blue-900 font-bold px-8 py-4 rounded-xl text-lg transition shadow-xl transform hover:-translate-y-1">
              Rezervă Acum
            </Link>
            <Link href="/services" className="bg-white/10 hover:bg-white/20 backdrop-blur-sm border border-white/30 text-white font-bold px-8 py-4 rounded-xl text-lg transition">
              Vezi Prețuri
            </Link>
          </div>
        </div>
      </header>

      {/* Pricing / Routes Section */}
      <section id="services" className="py-24 bg-white">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Destinații & Tarife</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">Prețurile sunt fixe în Euro. Plata se face în RON la cursul BNR din ziua cursei.</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {/* Budapesta Card */}
            <div className="bg-white rounded-3xl shadow-xl overflow-hidden border border-gray-100 hover:shadow-2xl transition duration-300 relative group">
              <div className="h-2 bg-blue-600 w-full"></div>
              <div className="p-8">
                <div className="flex justify-between items-start mb-6">
                  <div>
                    <h3 className="text-2xl font-bold text-gray-900">Budapesta</h3>
                    <p className="text-gray-500 text-sm">Aeroport Ferenc Liszt</p>
                  </div>
                  <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-xs font-bold uppercase">Zilnic</span>
                </div>
                
                <div className="flex items-baseline gap-1 mb-2">
                  <span className="text-5xl font-extrabold text-blue-600">€40</span>
                  <span className="text-gray-400">/pers</span>
                </div>
                <p className="text-xs text-gray-400 mb-8">*Echivalent RON la curs BNR</p>
                
                <ul className="space-y-4 mb-8">
                  <li className="flex items-center gap-3 text-gray-700"><CheckCircle size={20} className="text-green-500 flex-shrink-0"/> <span>Preluare de la adresă</span></li>
                  <li className="flex items-center gap-3 text-gray-700"><CheckCircle size={20} className="text-green-500 flex-shrink-0"/> <span>Bagaj de cală inclus</span></li>
                  <li className="flex items-center gap-3 text-gray-700"><CheckCircle size={20} className="text-green-500 flex-shrink-0"/> <span>Wi-Fi & Aer Condiționat</span></li>
                </ul>
                
                <Link href="/booking" className="block w-full bg-gray-50 hover:bg-blue-600 hover:text-white text-blue-900 font-bold py-4 rounded-xl transition text-center border border-gray-200 hover:border-blue-600">
                  Rezervă Budapesta
                </Link>
              </div>
            </div>

            {/* Viena Card */}
            <div className="bg-blue-900 rounded-3xl shadow-2xl overflow-hidden transform md:-translate-y-4 relative text-white">
              <div className="absolute top-0 right-0 bg-yellow-400 text-blue-900 text-xs font-bold px-4 py-2 rounded-bl-xl z-10">POPULAR</div>
              <div className="p-8">
                <div className="flex justify-between items-start mb-6">
                  <div>
                    <h3 className="text-2xl font-bold">Viena</h3>
                    <p className="text-blue-300 text-sm">Aeroport Schwechat</p>
                  </div>
                  <span className="bg-blue-800 text-blue-200 px-3 py-1 rounded-full text-xs font-bold uppercase">Zilnic</span>
                </div>
                
                <div className="flex items-baseline gap-1 mb-2">
                  <span className="text-5xl font-extrabold text-yellow-400">€65</span>
                  <span className="text-blue-300">/pers</span>
                </div>
                <p className="text-xs text-blue-400 mb-8">*Echivalent RON la curs BNR</p>
                
                <ul className="space-y-4 mb-8">
                  <li className="flex items-center gap-3 text-blue-100"><CheckCircle size={20} className="text-yellow-400 flex-shrink-0"/> <span>Preluare de la adresă</span></li>
                  <li className="flex items-center gap-3 text-blue-100"><CheckCircle size={20} className="text-yellow-400 flex-shrink-0"/> <span>Bagaj inclus</span></li>
                  <li className="flex items-center gap-3 text-blue-100"><CheckCircle size={20} className="text-yellow-400 flex-shrink-0"/> <span>Confort Premium</span></li>
                </ul>
                
                <Link href="/booking" className="block w-full bg-yellow-500 hover:bg-yellow-400 text-blue-900 font-bold py-4 rounded-xl transition text-center shadow-lg">
                  Rezervă Viena
                </Link>
              </div>
            </div>

            {/* Adaptive / VIP Card */}
            <div className="bg-white rounded-3xl shadow-xl overflow-hidden border border-gray-100 hover:shadow-2xl transition duration-300">
              <div className="h-2 bg-gray-800 w-full"></div>
              <div className="p-8">
                <div className="flex justify-between items-start mb-6">
                  <div>
                    <h3 className="text-2xl font-bold text-gray-900">VIP / Adaptiv</h3>
                    <p className="text-gray-500 text-sm">Curse Speciale</p>
                  </div>
                  <span className="bg-gray-100 text-gray-600 px-3 py-1 rounded-full text-xs font-bold uppercase">Flexibil</span>
                </div>
                
                <div className="mb-8">
                   <div className="mb-4">
                      <p className="font-bold text-gray-700">Transport Adaptiv</p>
                      <div className="flex items-baseline gap-1">
                        <span className="text-3xl font-bold text-gray-900">€1.30</span>
                        <span className="text-gray-500">/km</span>
                      </div>
                      <p className="text-xs text-gray-400">Timișoara → Exterior</p>
                   </div>
                   <div>
                      <p className="font-bold text-gray-700">VIP / Belgrad</p>
                      <span className="text-xl font-bold text-blue-600">Negociabil</span>
                      <p className="text-xs text-gray-400">În funcție de nr. persoane</p>
                   </div>
                </div>
                
                <ul className="space-y-4 mb-8">
                  <li className="flex items-center gap-3 text-gray-700"><CheckCircle size={20} className="text-gray-400 flex-shrink-0"/> <span>Mașină privată (Mazda CX-7)</span></li>
                  <li className="flex items-center gap-3 text-gray-700"><CheckCircle size={20} className="text-gray-400 flex-shrink-0"/> <span>Program flexibil</span></li>
                  <li className="flex items-center gap-3 text-gray-700"><CheckCircle size={20} className="text-gray-400 flex-shrink-0"/> <span>Opriri la cerere</span></li>
                </ul>
                
                <Link href="/contact" className="block w-full bg-white border-2 border-gray-200 hover:border-gray-800 text-gray-800 font-bold py-4 rounded-xl transition text-center">
                  Cere Ofertă
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Fleet Section */}
      <section className="py-24 bg-gray-50">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Flota Noastră</h2>
            <p className="text-gray-600">Siguranță și confort pentru fiecare călătorie.</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 max-w-7xl mx-auto">
            {/* Mazda CX-7 */}
            <div className="group bg-white rounded-2xl p-4 shadow-lg hover:shadow-xl transition">
              <div className="relative h-56 bg-gray-200 rounded-xl overflow-hidden mb-6">
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent z-10"></div>
                <img 
                  src="/images/mazda.jpg" 
                  alt="Mazda CX-7" 
                  className="w-full h-full object-cover transition duration-500 group-hover:scale-105"
                />
                <div className="absolute bottom-3 left-4 z-20 text-white">
                    <p className="font-bold text-sm uppercase tracking-wider">Comfort Standard</p>
                </div>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">Mazda CX-7</h3>
              <p className="text-gray-600 text-sm mb-4">SUV spațios și confortabil, perfect pentru familii sau grupuri mici. Echipat pentru distanțe lungi cu scaune confortabile și climatizare automată.</p>
              <div className="flex gap-3 text-xs text-gray-500 font-medium border-t pt-4">
                <span className="flex items-center gap-1"><Users size={14}/> 1-4 Pasageri</span>
                <span className="flex items-center gap-1"><Shield size={14}/> Asigurare Full</span>
              </div>
            </div>

            {/* Mercedes V-Class */}
            <div className="group bg-gray-900 rounded-2xl p-4 shadow-2xl hover:shadow-3xl transition transform md:-translate-y-4 border-2 border-gray-800 relative">
              <div className="absolute top-0 right-0 bg-yellow-500 text-gray-900 text-[10px] font-bold px-3 py-1 rounded-bl-lg z-30">VIP</div>
              <div className="relative h-56 bg-gray-800 rounded-xl overflow-hidden mb-6">
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent z-10"></div>
                <img 
                  src="/images/mercedes.jpg" 
                  alt="Mercedes V-Class" 
                  className="w-full h-full object-cover transition duration-500 group-hover:scale-105 opacity-90 group-hover:opacity-100"
                />
                <div className="absolute bottom-3 left-4 z-20 text-white">
                    <p className="font-bold text-sm uppercase tracking-wider text-yellow-400">VIP Luxury</p>
                </div>
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Mercedes V-Class</h3>
              <p className="text-gray-400 text-sm mb-4">Experiența supremă de călătorie. Interior piele, scaune individuale, spațiu generos și liniște absolută. Ideal pentru business sau VIP.</p>
              <div className="flex gap-3 text-xs text-gray-400 font-medium border-t border-gray-800 pt-4">
                <span className="flex items-center gap-1"><Users size={14}/> 1-6 Pasageri</span>
                <span className="flex items-center gap-1 text-yellow-500"><Shield size={14}/> Premium</span>
              </div>
            </div>

            {/* Ford Microbuz */}
            <div className="group bg-white rounded-2xl p-4 shadow-lg hover:shadow-xl transition">
              <div className="relative h-56 bg-gray-200 rounded-xl overflow-hidden mb-6">
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent z-10"></div>
                <img 
                  src="/images/ford.jpg" 
                  alt="Ford Transit Microbuz" 
                  className="w-full h-full object-cover transition duration-500 group-hover:scale-105"
                />
                <div className="absolute bottom-3 left-4 z-20 text-white">
                    <p className="font-bold text-sm uppercase tracking-wider">Grupuri Mari</p>
                </div>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">Ford Microbuz</h3>
              <p className="text-gray-600 text-sm mb-4">Soluția ideală pentru grupuri organizate. Spațiu extins pentru bagaje mari, aer condiționat individualizat și scaune rabatabile.</p>
              <div className="flex gap-3 text-xs text-gray-500 font-medium border-t pt-4">
                <span className="flex items-center gap-1"><Users size={14}/> 5-15 Pasageri</span>
                <span className="flex items-center gap-1"><Shield size={14}/> Licențiat</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Booking / Contact CTA */}
      <section id="booking" className="py-24 bg-blue-900 text-white relative overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full blur-3xl transform translate-x-1/2 -translate-y-1/2"></div>
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-yellow-500/10 rounded-full blur-3xl transform -translate-x-1/2 translate-y-1/2"></div>

        <div className="container mx-auto px-6 relative z-10 text-center">
          <h2 className="text-3xl md:text-5xl font-bold mb-8">Rezervă-ți locul acum</h2>
          <p className="text-xl text-blue-200 mb-12 max-w-2xl mx-auto">
            Suntem disponibili 24/7 pentru preluări comenzi. Contactează-ne telefonic sau pe WhatsApp pentru o confirmare rapidă.
          </p>
          
          <div className="flex flex-col md:flex-row justify-center items-center gap-6">
            <div className="bg-white p-8 rounded-2xl shadow-2xl w-full max-w-md transform transition hover:scale-105 duration-300">
              <p className="text-xs font-bold uppercase tracking-widest text-gray-400 mb-2">Dispecerat Non-Stop</p>
              <a href="tel:+40700000000" className="text-3xl md:text-4xl font-black text-blue-900 hover:text-blue-700 transition block mb-4">
                0700 000 000
              </a>
              <div className="flex justify-center gap-3">
                 <Link href="/booking" className="flex items-center gap-2 bg-yellow-500 hover:bg-yellow-600 text-blue-900 px-6 py-3 rounded-lg font-bold transition w-full justify-center">
                    Rezervă Online
                 </Link>
                 <a href="https://wa.me/40700000000" className="flex items-center gap-2 bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg font-bold transition w-full justify-center">
                    WhatsApp
                 </a>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-900 text-slate-400 py-16 border-t border-slate-800">
        <div className="container mx-auto px-6">
          <div className="grid md:grid-cols-4 gap-12 mb-12">
            <div className="col-span-1 md:col-span-2">
              <span className="text-2xl font-bold text-white block mb-4">TimTransExpress</span>
              <p className="max-w-xs">Partenerul tău de încredere pentru transferuri aeroportuare din zona de Vest a României.</p>
            </div>
            <div>
              <h4 className="text-white font-bold mb-4">Rute Populare</h4>
              <ul className="space-y-2">
                <li><Link href="/booking" className="hover:text-white transition">Timișoara - Budapesta</Link></li>
                <li><Link href="/booking" className="hover:text-white transition">Timișoara - Viena</Link></li>
                <li><Link href="/contact" className="hover:text-white transition">Timișoara - Belgrad</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-bold mb-4">Contact</h4>
              <ul className="space-y-2">
                <li>Timișoara, România</li>
                <li>contact@timtransexpress.ro</li>
                <li>+40 700 000 000</li>
              </ul>
            </div>
          </div>
          <div className="pt-8 border-t border-slate-800 flex flex-col md:flex-row justify-between items-center text-sm">
            <p>© 2025 TimTransExpress. Toate drepturile rezervate.</p>
            <div className="flex gap-6 mt-4 md:mt-0">
              <Link href="/terms" className="hover:text-white transition">Termeni și condiții</Link>
              <Link href="/gdpr" className="hover:text-white transition">GDPR</Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
