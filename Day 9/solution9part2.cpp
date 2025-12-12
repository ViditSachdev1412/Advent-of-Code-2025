// compile with: g++ -O2 -std=c++17 day9_part2.cpp -o day9_part2
#include <iostream>
#include <vector>
#include <algorithm>
#include <set>
#include <map>
#include <cmath>
using namespace std;
using ll = long long;
struct P { int x,y; };

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // Read input from stdin (or redirect from file)
    vector<P> red;
    string line;
    while (getline(cin, line)) {
        if (line.empty()) continue;
        if (line.size() > 0 && line[0] == '`') continue;
        if (line.find(',') == string::npos) continue;
        // parse x,y (robust to spaces)
        int comma = line.find(',');
        string sx = line.substr(0, comma);
        string sy = line.substr(comma+1);
        try {
            int x = stoi(sx);
            int y = stoi(sy);
            red.push_back({x,y});
        } catch(...) { continue; }
    }

    if (red.size() < 2) {
        cout << "Loaded " << red.size() << " points\nLargest rectangle area: 0\n";
        return 0;
    }

    int n = red.size();
    int miny = red[0].y, maxy = red[0].y;
    int minx = red[0].x, maxx = red[0].x;
    for (auto &p: red) {
        miny = min(miny, p.y);
        maxy = max(maxy, p.y);
        minx = min(minx, p.x);
        maxx = max(maxx, p.x);
    }

    // Height of rows we consider
    int H = maxy - miny + 1;
    // spans[y - miny] -> vector of [l,r] inclusive allowed x's on that integer row
    vector<vector<pair<int,int>>> spans(H);

    // 1) Add boundary tiles from straight segments between consecutive red tiles
    for (int i = 0; i < n; ++i) {
        P a = red[i];
        P b = red[(i+1)%n];
        if (a.x == b.x) {
            int x = a.x;
            int ya = min(a.y, b.y), yb = max(a.y, b.y);
            for (int y = ya; y <= yb; ++y) {
                spans[y - miny].push_back({x, x});
            }
        } else if (a.y == b.y) {
            int y = a.y;
            int xa = min(a.x, b.x), xb = max(a.x, b.x);
            spans[y - miny].push_back({xa, xb});
        } else {
            // The problem guarantees consecutive points share x or y.
            // If not, we ignore (defensive).
        }
    }

    // 2) Compute interior via vertical-edge crossings for each scanline y (tile centers at y+0.5)
    // Build vertical edges list
    struct VertEdge { int x, y1, y2; }; // crosses for y in [y1, y2) per half-open rule
    vector<VertEdge> vedges;
    for (int i = 0; i < n; ++i) {
        P a = red[i];
        P b = red[(i+1)%n];
        if (a.x == b.x) {
            int x = a.x;
            int y1 = a.y, y2 = b.y;
            if (y1 < y2) vedges.push_back({x, y1, y2});
            else if (y2 < y1) vedges.push_back({x, y2, y1});
            // zero-length edges still handled by boundary addition earlier
        }
    }

    // For each integer row y, find vertical edge crossings at scanline y+0.5
    for (int yi = 0; yi < H; ++yi) {
        int y = yi + miny;
        double scan_y = y + 0.5;
        vector<int> cross_x;
        cross_x.reserve(vedges.size());
        for (auto &e : vedges) {
            // Include crossing if edge spans scan_y with half-open [y1, y2)
            if ((double)e.y1 <= scan_y && scan_y < (double)e.y2) {
                cross_x.push_back(e.x);
            }
        }
        if (cross_x.empty()) continue;
        sort(cross_x.begin(), cross_x.end());
        // Pair up crossings into interior intervals
        for (size_t k = 0; k + 1 < cross_x.size(); k += 2) {
            int xl = cross_x[k];
            int xr = cross_x[k+1];
            // interior unit squares have integer x with center x+0.5 in (xl, xr)
            // That corresponds to x = xl .. xr-1 inclusive
            if (xl <= xr-1) spans[yi].push_back({xl, xr-1});
        }
    }

    // 3) For robustness: also add red points themselves (already covered by boundary) but ensure included
    for (auto &p : red) {
        spans[p.y - miny].push_back({p.x, p.x});
    }

    // 4) Merge spans on each row to get disjoint sorted inclusive intervals
    for (int yi = 0; yi < H; ++yi) {
        auto &v = spans[yi];
        if (v.empty()) continue;
        sort(v.begin(), v.end());
        vector<pair<int,int>> merged;
        merged.reserve(v.size());
        int cl = v[0].first, cr = v[0].second;
        for (size_t k = 1; k < v.size(); ++k) {
            if (v[k].first <= cr + 1) {
                cr = max(cr, v[k].second);
            } else {
                merged.push_back({cl, cr});
                cl = v[k].first; cr = v[k].second;
            }
        }
        merged.push_back({cl, cr});
        v.swap(merged);
    }

    // Utility: check if on row y (absolute), interval [L,R] inclusive is fully covered
    auto covered = [&](int y, int L, int R)->bool{
        if (y < miny || y > maxy) return false;
        auto &v = spans[y - miny];
        if (v.empty()) return false;
        // binary search for interval which might cover L
        int lo = 0, hi = (int)v.size()-1;
        while (lo <= hi) {
            int mid = (lo + hi) >> 1;
            if (v[mid].first <= L && v[mid].second >= L) {
                // candidate interval starts at v[mid].first
                return v[mid].second >= R; // must cover whole [L,R]
            } else if (v[mid].first > L) {
                hi = mid - 1;
            } else {
                lo = mid + 1;
            }
        }
        return false;
    };

    // 5) Build a fast map from y to a vector of rows that actually have any spans,
    //    but we need to check every row in rectangle, missing row => fail quickly.

    // 6) Check every pair of red tiles as opposite corners
    ll best_area = 0;
    pair<P,P> best_rect = {{0,0},{0,0}};

    for (int i = 0; i < n; ++i) {
        if (i % 50 == 0) {
            // optional progress: comment out if not desired
            // cerr << "Checking from red " << i << "/" << n << "\n";
            ;
        }
        for (int j = i+1; j < n; ++j) {
            P a = red[i], b = red[j];
            if (a.x == b.x || a.y == b.y) continue;
            int xl = min(a.x, b.x);
            int xr = max(a.x, b.x);
            int yb = min(a.y, b.y);
            int yt = max(a.y, b.y);
            bool ok = true;
            // Early quick check: for row yb and yt must be covered (these are small)
            if (!covered(yb, xl, xr) || !covered(yt, xl, xr)) continue;
            // Check all intermediate rows (inclusive)
            for (int y = yb; y <= yt; ++y) {
                if (!covered(y, xl, xr)) { ok = false; break; }
            }
            if (ok) {
                ll area = 1LL * (xr - xl + 1) * (yt - yb + 1);
                if (area > best_area) {
                    best_area = area;
                    best_rect = {a,b};
                }
            }
        }
    }

    cout << "Loaded " << n << " points\n";
    cout << "Largest rectangle area: " << best_area << "\n";
    if (best_area > 0) {
        cout << "Corners: (" << best_rect.first.x << "," << best_rect.first.y << ") and ("
                          << best_rect.second.x << "," << best_rect.second.y << ")\n";
    }
    return 0;
}
