import React, { useState, useEffect } from 'react';
import { ArrowLeft, ArrowRight, Zap, Eye, Search } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const implantList = [
  'Smith and Nephew LEGION',
  'Smith and Nephew ANTHEM',
  'Stryker SCORPIO',
  'Zimmer LPS Flex Knee GSF',
  'Zimmer Natural Knee II',
  'Zimmer NEXGEN',
  'Zimmer Oxford',
  'Zimmer persona',
  'Zimmer Vanguard',
  'Biomet AGC',
  'Depuy Attune',
  'Exatech Opterak Logic'
];

const implantImages = {
  'Smith and Nephew LEGION': 'https://balbharatiin.wordpress.com/wp-content/uploads/2025/09/legion.png',
  'Smith and Nephew ANTHEM': 'https://balbharatiin.wordpress.com/wp-content/uploads/2025/09/nephewanthem.jpeg',
  'Stryker SCORPIO': 'https://balbharatiin.wordpress.com/wp-content/uploads/2025/09/scorpio.png',
  'Zimmer LPS Flex Knee GSF': 'https://balbharatiin.wordpress.com/wp-content/uploads/2025/09/lps.jpeg',
  'Zimmer Natural Knee II': 'https://balbharatiin.wordpress.com/wp-content/uploads/2025/09/natural.jpeg',
  'Zimmer NEXGEN': 'https://balbharatiin.wordpress.com/wp-content/uploads/2025/09/nexgen.jpeg',
  'Zimmer Oxford': 'https://balbharatiin.wordpress.com/wp-content/uploads/2025/09/oxford.png',
  'Zimmer persona': 'https://balbharatiin.wordpress.com/wp-content/uploads/2025/09/persona.png',
  'Zimmer Vanguard': 'https://balbharatiin.wordpress.com/wp-content/uploads/2025/09/vanguard-1.png',
  'Biomet AGC': 'https://balbharatiin.wordpress.com/wp-content/uploads/2025/09/biomet.jpeg',
  'Depuy Attune': 'https://balbharatiin.wordpress.com/wp-content/uploads/2025/09/whatsapp-image-2025-09-13-at-2.57.27-pm.jpeg',
  'Exatech Opterak Logic': 'https://balbharatiin.wordpress.com/wp-content/uploads/2025/09/whatsapp-image-2025-09-13-at-2.46.02-pm.jpeg',
};

const Knee = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [hoveredCard, setHoveredCard] = useState(null);
const navigate = useNavigate();

  useEffect(() => {
    setIsVisible(true);
  }, []);

  const handleModelNavigation = () => {
    navigate('/knee-model');
  };

  const handleCardClick = (implantName) => {
    const implantRoute = implantName.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
    console.log(`Navigate to /${implantRoute}`);
  };

  const handleBackToMain = () => {
    console.log('Navigate to main');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50">
      {/* Floating background elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-purple-200/20 to-indigo-200/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-gradient-to-tr from-blue-200/20 to-cyan-200/20 rounded-full blur-3xl animate-pulse" style={{animationDelay: '1s'}}></div>
      </div>

      <div className="relative z-10 p-4 sm:p-6">
        <div className="max-w-7xl mx-auto">
          {/* Animated Header */}
          <div className={`mb-8 transition-all duration-1000 transform ${isVisible ? 'translate-y-0 opacity-100' : '-translate-y-10 opacity-0'}`}>
            <button 
              onClick={handleBackToMain}
              className="group flex items-center text-slate-600 hover:text-slate-900 mb-6 transition-all duration-300 hover:translate-x-1"
            >
              <ArrowLeft className="w-5 h-5 mr-2 transition-transform group-hover:-translate-x-1" />
              <span className="font-medium">Back to Main</span>
            </button>
            
            <div className="text-center">
              <h1 className="text-4xl sm:text-5xl font-black bg-gradient-to-r from-slate-900 via-purple-900 to-indigo-900 bg-clip-text text-transparent mb-4">
                Knee Implant Library
              </h1>
              <p className="text-slate-600 text-lg max-w-2xl mx-auto leading-relaxed">
                Explore cutting-edge knee implants with AI-powered identification
              </p>
            </div>
          </div>

          {/* Hero AI Section */}
          <div className={`mb-16 transition-all duration-1000 delay-300 transform ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
            <div className="relative bg-white/80 backdrop-blur-xl rounded-3xl p-8 shadow-2xl border border-white/20 overflow-hidden">
              {/* Animated background pattern */}
              <div className="absolute inset-0 bg-gradient-to-r from-purple-500/5 via-transparent to-indigo-500/5"></div>
              
              <div className="relative flex flex-col lg:flex-row items-center justify-center lg:space-x-12 space-y-8 lg:space-y-0">
                {/* 3D Floating Icon */}
                <div className="relative">
                  <div className="w-64 h-64 relative">
                    {/* Rotating ring */}
                    <div className="absolute inset-0 border-4 border-purple-200 rounded-full animate-spin" style={{animationDuration: '20s'}}></div>
                    <div className="absolute inset-4 border-2 border-indigo-200 rounded-full animate-spin" style={{animationDuration: '15s', animationDirection: 'reverse'}}></div>
                    
                    {/* Central icon */}
                    <div className="absolute inset-0 flex items-center justify-center">
                      <div className="w-24 h-24 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-2xl flex items-center justify-center shadow-2xl transform hover:scale-110 transition-transform duration-500">
                        <Zap className="w-12 h-12 text-white" />
                      </div>
                    </div>
                    
                    {/* Floating particles */}
                    <div className="absolute top-8 right-8 w-3 h-3 bg-purple-400 rounded-full animate-bounce"></div>
                    <div className="absolute bottom-12 left-12 w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{animationDelay: '0.5s'}}></div>
                    <div className="absolute top-16 left-8 w-2 h-2 bg-cyan-400 rounded-full animate-bounce" style={{animationDelay: '1s'}}></div>
                  </div>
                </div>

                {/* Content */}
                <div className="text-center lg:text-left max-w-xl">
                  <h2 className="text-3xl sm:text-4xl font-bold text-slate-900 mb-6 leading-tight">
                    AI-Powered Implant
                    <span className="bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent"> Recognition</span>
                  </h2>
                  <p className="text-slate-600 mb-8 text-lg leading-relaxed">
                    Upload your X-ray and watch our advanced AI instantly identify implant specifications with precision.
                  </p>
                  
                  <button
                    onClick={handleModelNavigation}
                    className="group relative bg-gradient-to-r from-purple-600 via-indigo-600 to-purple-700 text-white px-10 py-4 rounded-2xl font-bold text-lg shadow-2xl hover:shadow-purple-500/25 transition-all duration-300 transform hover:scale-105 hover:-translate-y-1 overflow-hidden"
                  >
                    {/* Button shine effect */}
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent transform -skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-700"></div>
                    
                    <div className="relative flex items-center space-x-3">
                      <Search className="w-6 h-6" />
                      <span>Identify Implant</span>
                      <ArrowRight className="w-6 h-6 transition-transform group-hover:translate-x-1" />
                    </div>
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Implant Grid */}
          <div className={`transition-all duration-1000 delay-500 transform ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
            <div className="relative bg-white/60 backdrop-blur-xl rounded-3xl p-8 shadow-2xl border border-white/20">
              <div className="flex items-center mb-8">
                <Eye className="w-8 h-8 text-purple-600 mr-3" />
                <h2 className="text-2xl font-bold text-slate-900">Implant Collection</h2>
              </div>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {implantList.map((implant, index) => (
                  <div
                    key={index}
                    className={`group relative bg-white/90 backdrop-blur-sm rounded-2xl p-6 shadow-lg hover:shadow-2xl cursor-pointer overflow-hidden transform transition-all duration-500 hover:scale-105 hover:-translate-y-2 ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}
                    style={{transitionDelay: `${600 + index * 100}ms`}}
                    onClick={() => handleCardClick(implant)}
                    onMouseEnter={() => setHoveredCard(index)}
                    onMouseLeave={() => setHoveredCard(null)}
                  >
                    {/* Hover gradient overlay */}
                    <div className="absolute inset-0 bg-gradient-to-br from-purple-500/0 to-indigo-500/0 group-hover:from-purple-500/5 group-hover:to-indigo-500/5 transition-all duration-500 rounded-2xl"></div>
                    
                    {/* Image container */}
                    <div className="relative aspect-square bg-gradient-to-br from-slate-50 to-indigo-50 rounded-3xl mb-4 overflow-hidden">
                      <div className="absolute inset-0 bg-gradient-to-br from-purple-100/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-3xl"></div>
                      <div className="w-full h-full p-4 flex items-center justify-center">
                        <img 
                          src={implantImages[implant]} 
                          alt={implant} 
                          className="max-w-full max-h-full object-contain transition-all duration-500 group-hover:scale-110 rounded-2xl"
                        />
                      </div>
                    </div>

                    {/* Content */}
                    <div className="relative z-10">
                      <h3 className="font-bold text-slate-900 mb-2 group-hover:text-purple-700 transition-colors duration-300 leading-tight">
                        {implant}
                      </h3>
                      
                      {/* Animated tags */}
                      <div className="flex flex-wrap gap-2">
                        {['X-ray', '3D', 'Specs'].map((tag, tagIndex) => (
                          <span 
                            key={tag}
                            className={`px-3 py-1 rounded-full text-xs font-medium transition-all duration-300 transform ${
                              hoveredCard === index 
                                ? 'bg-purple-100 text-purple-700 scale-105' 
                                : 'bg-slate-100 text-slate-600'
                            }`}
                            style={{transitionDelay: `${tagIndex * 100}ms`}}
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    </div>

                    {/* Corner decoration */}
                    <div className="absolute top-0 right-0 w-16 h-16 bg-gradient-to-bl from-purple-500/10 to-transparent rounded-bl-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Knee;
