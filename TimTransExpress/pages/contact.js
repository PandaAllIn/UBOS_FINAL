import Head from 'next/head';
import Link from 'next/link';
import { Phone, Mail, MapPin, Send } from 'lucide-react';

export default function Contact() {
  const handleSubmit = (e) => {
    e.preventDefault();
    alert('Mesajul a fost trimis! Îți vom răspunde în cel mai scurt timp.');
  };

  return (
    <div className="min-h-screen font-sans bg-slate-50">
      <Head>
        <title>Contact | TimTransExpress</title>
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

      <main className="container mx-auto px-6 py-12">
        <h1 className="text-4xl font-bold text-center text-blue-900 mb-4">Contactează-ne</h1>
        <p className="text-center text-gray-500 mb-16 max-w-2xl mx-auto">Suntem aici 24/7 pentru a răspunde întrebărilor tale despre rute, prețuri sau disponibilitate.</p>

        <div className="grid md:grid-cols-2 gap-12 max-w-5xl mx-auto">
          
          {/* Contact Info */}
          <div className="space-y-8">
            <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100">
              <h3 className="text-xl font-bold text-gray-900 mb-6">Informații de Contact</h3>
              
              <div className="space-y-6">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                    <Phone size={24} />
                  </div>
                  <div>
                    <p className="font-bold text-gray-900">Telefon / WhatsApp</p>
                    <a href="tel:+40700000000" className="text-blue-600 hover:underline text-lg">+40 700 000 000</a>
                    <p className="text-sm text-gray-500 mt-1">Disponibil 24/7</p>
                  </div>
                </div>

                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                    <Mail size={24} />
                  </div>
                  <div>
                    <p className="font-bold text-gray-900">Email</p>
                    <a href="mailto:contact@timtransexpress.ro" className="text-blue-600 hover:underline text-lg">contact@timtransexpress.ro</a>
                    <p className="text-sm text-gray-500 mt-1">Răspundem în max. 2 ore</p>
                  </div>
                </div>

                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                    <MapPin size={24} />
                  </div>
                  <div>
                    <p className="font-bold text-gray-900">Sediu</p>
                    <p className="text-gray-600">Timișoara, România</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Map Placeholder */}
            <div className="bg-gray-200 h-64 rounded-2xl overflow-hidden relative shadow-inner flex items-center justify-center">
              <div className="absolute inset-0 bg-gray-300 opacity-50"></div>
              <p className="text-gray-500 font-bold z-10 flex items-center gap-2"><MapPin/> Harta Google Maps</p>
              {/* Note: Insert real Google Maps iframe here later */}
            </div>
          </div>

          {/* Contact Form */}
          <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100">
            <h3 className="text-xl font-bold text-gray-900 mb-6">Trimite un Mesaj</h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Numele Tău</label>
                <input type="text" className="w-full px-4 py-3 rounded-lg border border-gray-200 focus:border-blue-500 outline-none transition" required placeholder="Ex: Popescu Andrei" />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Email sau Telefon</label>
                <input type="text" className="w-full px-4 py-3 rounded-lg border border-gray-200 focus:border-blue-500 outline-none transition" required placeholder="Cum te putem contacta?" />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Subiect</label>
                <select className="w-full px-4 py-3 rounded-lg border border-gray-200 focus:border-blue-500 outline-none transition bg-white">
                  <option>Rezervare nouă</option>
                  <option>Informații prețuri</option>
                  <option>Colaborare / Business</option>
                  <option>Altceva</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Mesaj</label>
                <textarea rows="4" className="w-full px-4 py-3 rounded-lg border border-gray-200 focus:border-blue-500 outline-none transition" required placeholder="Scrie mesajul tău aici..."></textarea>
              </div>

              <button type="submit" className="w-full bg-blue-900 hover:bg-blue-800 text-white font-bold py-4 rounded-xl transition flex items-center justify-center gap-2">
                Trimite Mesajul <Send size={18}/>
              </button>
            </form>
          </div>

        </div>
      </main>

      <footer className="bg-slate-900 text-slate-400 py-12 border-t border-slate-800 text-center">
        <p>© 2025 TimTransExpress</p>
      </footer>
    </div>
  );
}
