import Image from "next/image";

export default function About() {
  return (
    <section id="about" className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
              Why Choose VetLink?
            </h2>
            <p className="text-lg text-gray-600 mb-6">
              VetLink represents the future of pet healthcare, combining cutting-edge artificial intelligence 
              with veterinary expertise to provide comprehensive, personalized care for your beloved pets.
            </p>
            <div className="space-y-4">
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <div className="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center">
                    <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                </div>
                <div className="ml-3">
                  <h3 className="text-lg font-semibold text-gray-900">24/7 Health Monitoring</h3>
                  <p className="text-gray-600">Continuous monitoring and instant alerts for any health concerns</p>
                </div>
              </div>
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <div className="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center">
                    <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                </div>
                <div className="ml-3">
                  <h3 className="text-lg font-semibold text-gray-900">AI-Powered Diagnostics</h3>
                  <p className="text-gray-600">Advanced machine learning algorithms for accurate health assessments</p>
                </div>
              </div>
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <div className="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center">
                    <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                </div>
                <div className="ml-3">
                  <h3 className="text-lg font-semibold text-gray-900">Personalized Care Plans</h3>
                  <p className="text-gray-600">Tailored recommendations based on your pet's unique needs and health history</p>
                </div>
              </div>
            </div>
          </div>
          <div>
            <Image
              src="https://images.unsplash.com/photo-1601758228041-f3b2795255f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
              alt="Veterinarian with pet"
              width={600}
              height={400}
              className="rounded-lg shadow-xl"
            />
          </div>
        </div>
      </div>
    </section>
  );
}
