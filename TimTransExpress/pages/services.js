import Head from 'next/head';
import Link from 'next/link';
import { Plane, Car, UserCheck, Map, CheckCircle, ArrowRight, Phone } from 'lucide-react';

export default function Services() {
  return (
    <div className="min-h-screen font-sans bg-slate-50">
      <Head>
        <title>Servicii | TimTransExpress</title>
      </Head>

      {/* Navigation */}
      <nav className="bg-white shadow-sm sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <Link href="/" className="text-2xl font-black text-blue-900 tracking-tight">TimTransExpress</Link>
          <div className="flex gap-4">
             <Link href="/" className="text-gray-600 hover:text-blue-900 font-medium">Acasă</Link>
             <Link href="/booking" className="bg-blue-600 text-white px-4 py-2 rounded-lg font-bold hover:bg-blue-700 transition">Rezervă</Link>
          </div>
        </div>
      </nav>

      <main>
        {/* Header */}
        <section className="bg-blue-900 text-white py-20 text-center">
          <div className="container mx-auto px-6">
            <h1 className="text-4xl md:text-5xl font-extrabold mb-4">Serviciile Noastre</h1>
            <p className="text-xl text-blue-200 max-w-2xl mx-auto">Soluții complete de transport persoane, de la transferuri aeroportuare la curse private VIP.</p>
          </div>
        </section>

        {/* Services List */}
        <section className="py-20 container mx-auto px-6">
          <div className="space-y-20">

            {/* Service 1: Airport Transfer */}
            <div className="flex flex-col md:flex-row gap-12 items-center">
              <div className="flex-1">
                <div className="w-16 h-16 bg-blue-100 text-blue-600 rounded-2xl flex items-center justify-center mb-6">
                  <Plane size={32} />
                </div>
                <h2 className="text-3xl font-bold text-gray-900 mb-4">Transport Aeroport Standard</h2>
                <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                  Serviciul nostru principal, optimizat pentru confort și punctualitate. Asigurăm legătura zilnică între Timișoara și principalele aeroporturi din regiune.
                </p>
                <ul className="space-y-3 mb-8">
                  <li className="flex items-center gap-3 text-gray-700 font-medium"><CheckCircle className="text-green-500" size={20}/> Timișoara ⇄ Budapesta (€40)</li>
                  <li className="flex items-center gap-3 text-gray-700 font-medium"><CheckCircle className="text-green-500" size={20}/> Timișoara ⇄ Viena (€65)</li>
                  <li className="flex items-center gap-3 text-gray-700 font-medium"><CheckCircle className="text-green-500" size={20}/> Timișoara ⇄ Belgrad (La cerere)</li>
                </ul>
                <Link href="/booking" className="inline-flex items-center gap-2 text-blue-600 font-bold hover:underline text-lg">
                  Rezervă acum <ArrowRight size={20}/>
                </Link>
              </div>
              <div className="flex-1 h-80 bg-gray-200 rounded-3xl overflow-hidden shadow-xl">
                 <img src="/images/mazda.jpg" className="w-full h-full object-cover" alt="Transport Aeroport" />
              </div>
            </div>

            {/* Service 2: Adaptive Transport */}
            <div className="flex flex-col md:flex-row-reverse gap-12 items-center">
              <div className="flex-1">
                <div className="w-16 h-16 bg-orange-100 text-orange-600 rounded-2xl flex items-center justify-center mb-6">
                  <Map size={32} />
                </div>
                <h2 className="text-3xl font-bold text-gray-900 mb-4">Transport Adaptiv (Oriunde)</h2>
                <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                  Ai nevoie să ajungi într-o altă localitate? Oferim transport privat la cerere, oriunde în Europa sau în țară, cu plecare din Timișoara.
                </p>
                <div className="bg-orange-50 p-6 rounded-2xl border border-orange-100 mb-8">
                  <p className="text-orange-900 font-bold text-lg mb-1">Tarif Transparent</p>
                  <div className="flex items-baseline gap-2">
                    <span className="text-4xl font-black text-orange-600">€1.30</span>
                    <span className="text-gray-600">/ km</span>
                  </div>
                  <p className="text-sm text-gray-500 mt-2">Calculat pentru distanța totală parcursă.</p>
                </div>
                <Link href="/booking" className="inline-flex items-center gap-2 text-orange-600 font-bold hover:underline text-lg">
                  Solicită ofertă <ArrowRight size={20}/>
                </Link>
              </div>
              <div className="flex-1 h-80 bg-gray-200 rounded-3xl overflow-hidden shadow-xl">
                 <img src="https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?q=80&w=2021&auto=format&fit=crop" className="w-full h-full object-cover" alt="Road Trip" />
              </div>
            </div>

            {/* Service 3: VIP & Business */}
            <div className="flex flex-col md:flex-row gap-12 items-center">
              <div className="flex-1">
                <div className="w-16 h-16 bg-gray-900 text-white rounded-2xl flex items-center justify-center mb-6">
                  <UserCheck size={32} />
                </div>
                <h2 className="text-3xl font-bold text-gray-900 mb-4">VIP & Business Class</h2>
                <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                  Pentru clienții care apreciază intimitatea și confortul suprem. Închiriază întreaga mașină (Mercedes V-Class sau SUV) doar pentru tine și partenerii tăi.
                </p>
                <ul className="space-y-3 mb-8">
                  <li className="flex items-center gap-3 text-gray-700"><CheckCircle className="text-gray-900" size={20}/> Șofer personal la dispoziție</li>
                  <li className="flex items-center gap-3 text-gray-700"><CheckCircle className="text-gray-900" size={20}/> Program flexibil 100%</li>
                  <li className="flex items-center gap-3 text-gray-700"><CheckCircle className="text-gray-900" size={20}/> Discreție totală</li>
                </ul>
                <Link href="/contact" className="inline-flex items-center gap-2 text-gray-900 font-bold hover:underline text-lg">
                  Contactează-ne pentru ofertă <ArrowRight size={20}/>
                </Link>
              </div>
              <div className="flex-1 h-80 bg-gray-900 rounded-3xl overflow-hidden shadow-xl">
                 <img src="/images/mercedes.jpg" className="w-full h-full object-cover opacity-90" alt="VIP Transport" />
              </div>
            </div>

          </div>
        </section>

        {/* CTA */}
        <section className="bg-yellow-400 py-16 text-center">
           <div className="container mx-auto px-6">
             <h2 className="text-3xl font-bold text-blue-900 mb-6">Ai o cerere specială?</h2>
             <p className="text-xl text-blue-800 mb-8 max-w-2xl mx-auto">Suntem flexibili. Sună-ne și găsim o soluție pentru transportul tău.</p>
             <a href="tel:+40700000000" className="inline-flex items-center gap-2 bg-blue-900 text-white px-8 py-4 rounded-xl font-bold hover:bg-blue-800 transition shadow-lg">
               <Phone size={20}/> Sună la Dispecerat
             </a>
           </div>
        </section>
      </main>
      
      <footer className="bg-slate-900 text-slate-400 py-12 border-t border-slate-800 text-center">
        <p>© 2025 TimTransExpress</p>
      </footer>
    </div>
  );
}
