#include <iostream>
#include <fstream>
#include <map>
using namespace std;

int main(){
    ifstream corpus;
    corpus.open("corpus.txt");
    if (!corpus) {
        cerr << "Unable to open file datafile.txt";
        exit(1);   // call system to stop
    }   
    
    int cont = 0;
        
    string s;
    map <string, int> M;
    while (corpus >> s) {
        
        if(s[0] < 'A' or s[0] > 'Z') continue;
        
        auto it = M.find(s);
        if ( it == M.end()) M.insert(make_pair(s, 1));
        else ++M[s];
    }
    corpus.close();
    for (auto it = M.begin(); it != M.end(); ++it){
        if( it -> second >= 1000){
             cout << it -> first << ": " << it -> second << " time(s)" << endl;
             ++cont;
         }
    }
    
    cout << endl << "Num: " << cont << endl;

}
