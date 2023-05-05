#include<iostream>
#include <stdio.h>
#include <map>
#include <vector>

using namespace std;

vector<int> sosedni_cleni(int x){
    vector<int> sosedi;
    int i = 0;
    int digits[10];

    if(x == 0){
        digits[0] = 0;
        i = 1;
    }
    else{
        while(x != 0){
            digits[i] = x % 10;
            x = x / 10;
            i++;
        }
    }

    for(int j = 0; j <= i; j++){

        // ce dodamo digit
        for(int d = 0; d <= 9; d++){
            int st = 0;
            int exp = 1;

            for(int k = 0; k < i; k++){
                if(k == j){
                    st += d * exp;
                    exp = exp * 10;
                }
                
                st += digits[k] * exp;
                exp = exp * 10;
            }       

            if(j == i)
                st += d * exp;

            sosedi.push_back(st);
        }

        // ce manjka digit
        int st = 0;
        int exp = 1;

        for(int k = 0; k < i; k++){
            if(k != j){
                st += digits[k] * exp;
                exp = exp * 10;
            }
        }       

        sosedi.push_back(st);

        // ce zamenjamo digit
        if (j < i){
            for(int d = 0; d <= 9; d++){
                int st = 0;
                int exp = 1;

                for(int k = 0; k < i; k++){
                    if(k == j)
                        st += d * exp;
                    else
                        st += digits[k] * exp;

                    exp = exp * 10;
                }       

                sosedi.push_back(st);
            }
        }
    }

    return sosedi;
}

int main(){
    int st_x = 0;
    int max_len[30000];
    int zaporedje[30000];
    map<int,int> index;
    vector<vector<int>> sosedi = vector<vector<int>>(30000);

    while(scanf("%d", &zaporedje[st_x]) != EOF){
        index[zaporedje[st_x]] = st_x;
        st_x++;
    }

    for (int i = 0; i < st_x; i++){
        vector<int> tipkarska_napake = sosedni_cleni(zaporedje[i]);

        for (int j = 0; j < tipkarska_napake.size(); j++){
            if (index.find(tipkarska_napake[j]) != index.end() && index[tipkarska_napake[j]] < i)
                sosedi[i].push_back(index[tipkarska_napake[j]]);
        }

        max_len[i] = 1;
    }
   
    int izhod = 1;

    for (int i = 1; i < st_x; i++){
        for (int j = 0; j < sosedi[i].size(); j++)
            max_len[i] = max(max_len[i], max_len[sosedi[i][j]] + 1);
        
        izhod = max(izhod, max_len[i]);
    }

    cout << izhod << endl;
    return 0;
}