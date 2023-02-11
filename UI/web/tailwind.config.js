module.exports = {
  content: ["./src/**/*.{html,js,ts,tsx,jsx,mjs}"],
  theme: {
    screens: {
			'sm': '640px',
			'md': '1100px',
			'lg': '1224px',
			'xl': '1380px',
			'2xl': '1536px',
		},
    extend: {
      colors:{
        'clr-navy':'#16182A',
        'clr-red':'#F95C75',
      },
      fontFamily: {
        'lato':['Lato','sans-serif'],
        'roboto':['Roboto', 'sans-serif'],
        'bebas':['Bebas Neue', 'cursive']
			},
      backgroundImage:{

      },
      transitionProperty: {
        'height': 'height',
        'width': 'width',
        'spacing': 'margin, padding',
      },
    },
  },
  variants: {
    extend: {
      width: ['responsive', 'hover', 'focus', 'group-hover'],
      scale:['responsive','hover','group-hover'],
      display: ['group-hover'],
    },
  },
  plugins: [],
}