const year = new Date().getFullYear();

const config = {

  backend:  'http://localhost:8000',
  frontend: 'http://localhost:8080',
  timeout:   5000, // ms
  cors:      true, // cross-origin resource sharing

  band: {
    name:     'Musikverein Dingenskirchen e.V.',
    nickname: 'MV',
    website:  'http://musikverein-dingenskirchen.de',
    email:    'info@musikverein-dingenskirchen.de'
  },

  bandbase: {
    name:      'Bandbase Frontend',
    version:   '2.0',
    copyright: '&copy; ' + 2015 + '&ndash;' + year + ' by ' +
               '<a href="https://github.com/jurihock" class="link-secondary">github.com/jurihock</a>'
  }

};

export default config;
