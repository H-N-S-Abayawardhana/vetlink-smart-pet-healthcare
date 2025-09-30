import Image from "next/image";

export default function Testimonials() {
  return (
    <section id="testimonials" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            What Pet Owners Say
          </h2>
          <p className="text-xl text-gray-600">
            Real stories from pet owners who trust VetLink with their pets' health
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div className="bg-gray-50 p-6 rounded-xl hover:shadow-lg transition-shadow duration-300">
            <div className="flex items-center mb-4">
              <Image
                src="https://images.unsplash.com/photo-1544005313-94ddf0286df2?ixlib=rb-4.0.3&auto=format&fit=crop&w=100&q=80"
                alt="Sarah Johnson"
                width={50}
                height={50}
                className="rounded-full object-cover"
              />
              <div className="ml-4">
                <h4 className="font-semibold text-gray-900">Sarah Johnson</h4>
                <p className="text-gray-600">Dog Owner</p>
              </div>
            </div>
            <p className="text-gray-700 italic">
              "VetLink's skin detection feature helped me catch my dog's early-stage dermatitis. 
              The AI recommendations were spot-on and saved us a costly vet visit!"
            </p>
          </div>
          
          <div className="bg-gray-50 p-6 rounded-xl hover:shadow-lg transition-shadow duration-300">
            <div className="flex items-center mb-4">
              <Image
                src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=100&q=80"
                alt="Mike Chen"
                width={50}
                height={50}
                className="rounded-full object-cover"
              />
              <div className="ml-4">
                <h4 className="font-semibold text-gray-900">Mike Chen</h4>
                <p className="text-gray-600">Cat Owner</p>
              </div>
            </div>
            <p className="text-gray-700 italic">
              "The anomaly detection system alerted me when my cat started limping. 
              Early detection meant faster treatment and a quicker recovery."
            </p>
          </div>
          
          <div className="bg-gray-50 p-6 rounded-xl hover:shadow-lg transition-shadow duration-300">
            <div className="flex items-center mb-4">
              <Image
                src="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-4.0.3&auto=format&fit=crop&w=100&q=80"
                alt="Emily Rodriguez"
                width={50}
                height={50}
                className="rounded-full object-cover"
              />
              <div className="ml-4">
                <h4 className="font-semibold text-gray-900">Emily Rodriguez</h4>
                <p className="text-gray-600">Multi-Pet Owner</p>
              </div>
            </div>
            <p className="text-gray-700 italic">
              "The AI diet plans have been a game-changer for my pets' health. 
              Each of my three pets has a personalized nutrition plan that works perfectly!"
            </p>
          </div>

          <div className="bg-gray-50 p-6 rounded-xl hover:shadow-lg transition-shadow duration-300">
            <div className="flex items-center mb-4">
              <Image
                src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&auto=format&fit=crop&w=100&q=80"
                alt="David Thompson"
                width={50}
                height={50}
                className="rounded-full object-cover"
              />
              <div className="ml-4">
                <h4 className="font-semibold text-gray-900">David Thompson</h4>
                <p className="text-gray-600">Golden Retriever Owner</p>
              </div>
            </div>
            <p className="text-gray-700 italic">
              "The health monitoring dashboard gives me peace of mind. I can track my dog's activity levels, 
              sleep patterns, and overall wellness trends all in one place."
            </p>
          </div>

          <div className="bg-gray-50 p-6 rounded-xl hover:shadow-lg transition-shadow duration-300">
            <div className="flex items-center mb-4">
              <Image
                src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?ixlib=rb-4.0.3&auto=format&fit=crop&w=100&q=80"
                alt="Lisa Park"
                width={50}
                height={50}
                className="rounded-full object-cover"
              />
              <div className="ml-4">
                <h4 className="font-semibold text-gray-900">Lisa Park</h4>
                <p className="text-gray-600">Persian Cat Owner</p>
              </div>
            </div>
            <p className="text-gray-700 italic">
              "VetLink's grooming recommendations are fantastic! My Persian cat's coat has never looked better. 
              The AI suggested the perfect grooming schedule and products."
            </p>
          </div>

          <div className="bg-gray-50 p-6 rounded-xl hover:shadow-lg transition-shadow duration-300">
            <div className="flex items-center mb-4">
              <Image
                src="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?ixlib=rb-4.0.3&auto=format&fit=crop&w=100&q=80"
                alt="James Wilson"
                width={50}
                height={50}
                className="rounded-full object-cover"
              />
              <div className="ml-4">
                <h4 className="font-semibold text-gray-900">James Wilson</h4>
                <p className="text-gray-600">Senior Pet Owner</p>
              </div>
            </div>
            <p className="text-gray-700 italic">
              "As my dog ages, VetLink's senior care features have been invaluable. The medication reminders 
              and health alerts help me provide the best care for my 12-year-old companion."
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
