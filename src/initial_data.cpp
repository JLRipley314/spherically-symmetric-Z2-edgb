#include <iomanip>
using std::setprecision;
using std::setw;
#include <iostream>
using std::cout;
using std::endl;
#include <cassert> 
#include <cmath>
using std::exp;
using std::pow;
#include <vector>
using std::vector;
#include "initial_data.hpp"
#include "sim_params.hpp"
#include "field.hpp"
/*===========================================================================*/
void set_initial_data(
	const Sim_params &sp,
	const vector<double> &rvec,
	Field &al,Field &ze,
	Field &f, Field &p, Field &q)
{
	double amp= sp.amp;
	double r_l= sp.r_l;
	double r_u= sp.r_u;
	
	double max_val= 0;
	
	double charge= sp.charge;

/*-------------------------------------------------------------------------*/
	if (sp.initial_data_type=="bump_with_bh") {
		assert(r_u>r_l);
		for (int i=sp.initial_exc_i; i<sp.nx-1; ++i) {
			double r= rvec[i];
			if ((r>r_l)
			&&  (r<r_u)
			) {
				double bump= exp(-1./(r_u-r))*exp(-1./(r-r_l)); 

				f.n[i]= pow(r-r_l,2)*pow(r_u-r,2)*bump; 
				p.n[i]= 0;
				q.n[i]= (
					2*(r-r_l)*pow(r_u-r,2)
				-	2*pow(r-r_l,2)*(r_u-r)
				+	pow(r_u-r,2)
				-	pow(r-r_l,2)
				)*bump;
			} else {
				f.n[i]= 0;
				p.n[i]= 0;
				q.n[i]= 0;
			}
			max_val= (fabs(f.n[i])>max_val) ? fabs(f.n[i]) : max_val;

			al.n[i]= 1;
			ze.n[i]= pow(2*sp.bh_mass/r,0.5);
		}
/* rescale so amp is actual maximum val */
		for (int i=0; i<sp.nx-1; ++i) {
			f.n[i]*= amp/max_val;
			q.n[i]*= amp/max_val;
			p.n[i]*= amp/max_val;
		}
/*-------------------------------------------------------------------------*/
	} else 	
	if (sp.initial_data_type=="scalarized_bh") {
		for (int i=sp.initial_exc_i; i<sp.nx-1; ++i) {
			double r= rvec[i];

			f.n[i]= (charge/r)+(charge*sp.bh_mass/pow(r,2)); 
			q.n[i]= -charge/pow(r,2)-(2*charge*sp.bh_mass/pow(r,3));

			al.n[i]= 1;
			ze.n[i]= pow(2*sp.bh_mass/r,0.5);

			p.n[i]= -ze.n[i]*q.n[i];
		}
/*-------------------------------------------------------------------------*/
	} else {
		cout << "ERROR: initial_data_type " << sp.initial_data_type << " did not match" << endl;
		std::quick_exit(0);
	}
/*-------------------------------------------------------------------------*/
	for (int i=0; i<sp.nx; ++i) {
		f.inter_2[i]= f.n[i];
		f.inter_3[i]= f.n[i];
		f.inter_4[i]= f.n[i];
		f.np1[i]=     f.n[i];

		p.inter_2[i]= p.n[i];
		p.inter_3[i]= p.n[i];
		p.inter_4[i]= p.n[i];
		p.np1[i]=     p.n[i];

		q.inter_2[i]= q.n[i];
		q.inter_3[i]= q.n[i];
		q.inter_4[i]= q.n[i];
		q.np1[i]=     q.n[i];

		al.inter_2[i]= al.n[i];
		al.inter_3[i]= al.n[i];
		al.inter_4[i]= al.n[i];
		al.np1[i]=     al.n[i];

		ze.inter_2[i]= ze.n[i];
		ze.inter_3[i]= ze.n[i];
		ze.inter_4[i]= ze.n[i];
		ze.np1[i]=     ze.n[i];
	}
/*-------------------------------------------------------------------------*/
	return;
}
