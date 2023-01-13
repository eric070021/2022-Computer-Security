#include <iostream>
#include <vector>

using namespace std;

int result[] = {1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1};

class LFSR{
	public:
		unsigned long long tap, state;
		int size;
		LFSR(unsigned long long state, unsigned long long tap, int size):
			state(state), tap(tap), size(size){}

		int getbit(){
			int next_bit = __builtin_popcountll(tap & state) & 1;
			int result = state & 1;
			state = state >> 1 | next_bit << (size-1);
			return result;
		}
};

double correlation(int a[]){
	int count = 0;
	for(int i = 0; i < 200; i++){
		if(result[i+232] == a[i]) count++;
	}
	return (double)count / 200;
}

vector<unsigned long long> cal_state(unsigned long long tap, int size){
	vector<unsigned long long> vec;
	int output[200];
	for(unsigned long long state = 0; state < (1ll << size); state++){
		LFSR lfsr = LFSR(state, tap, size);
		for(int i = 0; i < 232; i++){
			lfsr.getbit();
		}
		
		for(int i = 0; i < 200; i++){
			output[i] = lfsr.getbit();
		}
		if(correlation(output) >= 0.74){
			vec.emplace_back(state);
		}
	}
	
	return vec;
}

int main(){
	unsigned long long tap[] = {1 | 1 << 13 | 1 << 16 | 1 << 26, 1 | 1 << 5 | 1 << 7 | 1 << 22, 1 | 1 << 17 | 1 << 19 | 1 << 24};
	unsigned long long origin_state[3];
	int size[] = {27, 23, 25};
	vector<unsigned long long> state0, state1, state2;
	state1 = cal_state(tap[1], size[1]);
	state2 = cal_state(tap[2], size[2]);
	int output[200];

	for(unsigned long long _state1 : state1){
		for(unsigned long long _state2 : state2){
			for(unsigned long long _state0 = 0; _state0 < (1ll << size[0]); _state0++){
				LFSR lfsr0 = LFSR(_state0, tap[0], size[0]);
				LFSR lfsr1 = LFSR(_state1, tap[1], size[1]);
				LFSR lfsr2 = LFSR(_state2, tap[2], size[2]);
				
				for(int i = 0; i < 232; i++){
					lfsr0.getbit();
					lfsr1.getbit();
					lfsr2.getbit();
				}
				int x0, x1, x2;
				for(int i = 0; i < 200; i++){
					x0 = lfsr0.getbit();
					x1 = lfsr1.getbit();
					x2 = lfsr2.getbit();
					output[i] = x0 ? x1 : x2;
				}
				if(correlation(output) >= 1){
					origin_state[0] = _state0;
					origin_state[1] = _state1;
					origin_state[2] = _state2;
					goto final;
				}
			}
		}
	}

	final:
		LFSR lfsr0 = LFSR(origin_state[0], tap[0], size[0]);
		LFSR lfsr1 = LFSR(origin_state[1], tap[1], size[1]);
		LFSR lfsr2 = LFSR(origin_state[2], tap[2], size[2]);
		unsigned char flag[30] = {0};
		int o, x0, x1, x2;
		for(int i = 0; i < 29; i++){
			for(int j = 0; j < 8; j++){
				x0 = lfsr0.getbit();
				x1 = lfsr1.getbit();
				x2 = lfsr2.getbit();
				o = x0 ? x1 : x2;
				flag[i] |= (result[i*8 + j] ^ o) << (7-j);
			}
		}
		
		cout << flag;
}