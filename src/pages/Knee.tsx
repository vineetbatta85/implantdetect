import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, ArrowRight } from 'lucide-react';

const implantList = [
  'Microport MEDIAPIVOT',
  'Smith and Nephew JOURNEY',
  'Smith and Nephew LEGION',
  'Smith and Nephew ANTHEM',
  'Smith and Nephew GENESIS II',
  'Smith and Nephew Genesis PS',
  'Smith and Nephew TC PLUS SOLUTION',
  'Stryker NRG',
  'Stryker SCORPIO',
  'Stryker TRIATHLON',
  'TTK Healthcare BUCHEL PAPPAS',
  'Zimmer INSALL BURSTEIN I',
  'Zimmer LPS Flex Knee GSF',
  'Zimmer biomet LCCK',
  'Zimmer Natural Knee II',
  'Zimmer NEXGEN',
  'Zimmer NK II',
  'Zimmer Oxford',
  'Zimmer persona',
  'Zimmer UKS (ZUK)',
  'Zimmer Vanguard',
  'Aesculap Columbus',
  'Anika unicap',
  'BIOIMPIANTI K mod',
  'Biomet AGC',
  'Depuy AMK',
  'Depuy Attune',
  'Depuy COORDINATE',
  'Depuy LCS',
  'Depuy PFC SIGMA',
  'DJO 3D Knee',
  'Exatech Opterak Logic',
  'Howmedica DURACON TS',
  'Implantcast ACS PS fixed bearing',
  'INTERMEDICS Natural Knee',
  'Kyocera ACTIYAS',
  'Kyocera INITIA PS',
  'Kyocera TRIBRID',
  'Link endomodel',
  'Link Gemini SL',
  'Meril life FREEDOM KNEE'
];

const Knee = () => {
  const navigate = useNavigate();

  const handleModelNavigation = () => {
    console.log('Launching AI Model...');
    navigate('/knee-model');
  };

  const handleCardClick = (implantName: string) => {
    console.log(`Navigating to ${implantName}`);
    const implantRoute = implantName.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
    navigate(`/${implantRoute}`);
  };

  const handleBackToMain = () => {
    console.log('Back to Main');
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <button 
            onClick={handleBackToMain}
            className="flex items-center text-gray-600 hover:text-gray-800 mb-4"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Back to Main
          </button>
          
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">Knee Implant Library</h1>
            <p className="text-gray-600">Browse knee implant X-ray images, 3D models, and specifications</p>
          </div>
        </div>

        {/* AI Model Launch Section */}
        <div className="mb-12 text-center">
          <div className="bg-white rounded-3xl p-8 shadow-lg max-w-4xl mx-auto">
            <div className="flex items-center justify-center space-x-8">
              {/* Illustration placeholder (you can replace with a knee-specific animation later) */}
              <div className="w-64 h-64 bg-gradient-to-br from-blue-50 to-green-50 rounded-full flex items-center justify-center animate-pulse">
                <div className="w-32 h-32 bg-blue-200 rounded-lg"></div>
              </div>

              {/* Text Content */}
              <div className="text-left">
                <h2 className="text-3xl font-bold text-gray-900 mb-4">
                  Identify your knee implant with our AI technology
                </h2>
                <p className="text-gray-600 mb-6 text-lg">
                  Upload your X-ray image and let our advanced AI model identify the implant type, manufacturer, and specifications instantly.
                </p>
                <button
                  onClick={handleModelNavigation}
                  className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all font-semibold text-lg shadow-lg hover:shadow-xl transform hover:scale-105 flex items-center space-x-2"
                >
                  <span>Identify your implant</span>
                  <div className="w-6 h-6 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
                    <ArrowRight className="w-4 h-4" />
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Knee Implant Library Grid */}
        <div className="bg-white rounded-3xl p-8 shadow-lg">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Knee Implant Library</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {implantList.map((implant, index) => (
              <div
                key={index}
                className="bg-white border-2 border-gray-200 rounded-2xl p-6 shadow-md hover:shadow-lg transition-all duration-300 cursor-pointer hover:border-blue-300 group"
                onClick={() => handleCardClick(implant)}
              >
                <div className="aspect-square bg-gradient-to-br from-green-50 to-blue-50 rounded-xl mb-4 flex items-center justify-center">
                  <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
                    <div className="w-8 h-4 bg-green-600 rounded-md"></div>
                  </div>
                </div>
                <h3 className="text-lg font-bold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">
                  {implant}
                </h3>
                <p className="text-sm text-gray-600 mb-4">
                  View X-rays, specs, and 3D models
                </p>
                <div className="flex space-x-2">
                  <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded-full text-xs">
                    X-ray
                  </span>
                  <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded-full text-xs">
                    3D
                  </span>
                  <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded-full text-xs">
                    Specs
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Knee;

