import Image from "next/image";

export default function Features() {
  return (
    <section id="features" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Our Revolutionary Features
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Four powerful AI-driven systems working together to provide comprehensive pet healthcare
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Feature 1: Skin Care Detection */}
          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100 transform hover:-translate-y-2">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Skin Care Detection</h3>
              <p className="text-gray-600 mb-4">
                Advanced AI analyzes skin conditions and provides stage-based first aid recommendations for immediate care.
              </p>
              <Image
                src="https://images.unsplash.com/photo-1551601651-2a8555f1a136?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"
                alt="Pet skin care"
                width={200}
                height={150}
                className="rounded-lg mx-auto"
              />
            </div>
          </div>

          {/* Feature 2: Anomaly Detection */}
          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100 transform hover:-translate-y-2">
            <div className="text-center">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Anomaly Detection</h3>
              <p className="text-gray-600 mb-4">
                Intelligent monitoring system detects unusual behaviors including limping patterns and alerts you to potential health issues.
              </p>
              <Image
                src="https://images.unsplash.com/photo-1583337130417-3346a1be7dee?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"
                alt="Pet monitoring"
                width={200}
                height={150}
                className="rounded-lg mx-auto"
              />
            </div>
          </div>

          {/* Feature 3: AI Diet Plans */}
          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100 transform hover:-translate-y-2">
            <div className="text-center">
              <div className="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">AI Diet Plans</h3>
              <p className="text-gray-600 mb-4">
                Personalized nutrition recommendations based on your pet's breed, age, weight, and health conditions.
              </p>
              <Image
                src="https://images.unsplash.com/photo-1583337130417-3346a1be7dee?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"
                alt="Pet nutrition"
                width={200}
                height={150}
                className="rounded-lg mx-auto"
              />
            </div>
          </div>

          {/* Feature 4: Intelligent Pharmacy */}
          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100 transform hover:-translate-y-2">
            <div className="text-center">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Intelligent Pharmacy</h3>
              <p className="text-gray-600 mb-4">
                Smart pharmacy matching system finds the best medications and dosages for your pet's specific needs.
              </p>
              <Image
                src="https://images.unsplash.com/photo-1587854692152-cbe660dbde88?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"
                alt="Pet pharmacy"
                width={200}
                height={150}
                className="rounded-lg mx-auto"
              />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
