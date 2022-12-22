#include <bits/stdc++.h>

using namespace std;

//---------------------------------------------------

int modInverse(int A, int M) // O(logM)
{
    int m0 = M;
    int y = 0, x = 1;
 
    if (M == 1)
        return 0;
 
    while (A > 1) {
        // q is quotient
        int q = A / M;
        int t = M;
 
        // m is remainder now, process same as
        // Euclid's algo
        M = A % M, A = t;
        t = y;
 
        // Update y and x
        y = x - q * y;
        x = t;
    }
 
    // Make x positive
    if (x < 0)
        x += m0;
 
    return x;
}

//---------------------------------------------------

int main() { // O(m + n + logt)
    int st_primerov; cin >> st_primerov;
    
    for (int j=0; j < st_primerov; j++){
        
        int n, m, q, t; cin >> n >> m >> q >> t;
        
        vector<long long int> podkupnine;
        vector<long long int> potence_q;
        
        potence_q.push_back(1); // q ** 0
        
        for (int i=1; i <= n; i++){ // O(n)
            podkupnine.push_back(0);
            potence_q.push_back((potence_q[i-1] * q) % t);
        }
        
        for (int i=0; i < m; i++){ // O(m)
            int a, b, c; cin >> a >> b >> c;
            podkupnine[a-1] += c;
            if (b < n){
                podkupnine[b] -= c;
            }
        }
        
        long long int vsota = 0;
        
        for (int i=0; i < n; i++){ // O(n)
            vsota += podkupnine[i] * potence_q[i] 
                                   * (potence_q[n-i] - 1);
            vsota %= t;
        } 
        
        vsota *= (modInverse(q-1, t) % t); // O(logt)
        vsota %= t;
        
        while (vsota < 0){
            vsota += t;
        }
        
        cout << vsota << endl;
    }
    
    return 0;
}
