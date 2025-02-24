#!/usr/bin/python3

# Copyright 2021 The VGC Developers
# See the COPYRIGHT file at the top-level directory of this distribution
# and at https://github.com/vgc/vgc/blob/master/COPYRIGHT
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from math import inf, pi
import locale
import unittest

from vgc.geometry import Vec2d, Vec2f, Vec2dArray

Vec2Types = [Vec2d, Vec2f]


class TestVec2(unittest.TestCase):

    def testDefaultConstructor(self):
        for Vec2x in Vec2Types:
            v = Vec2x()
            self.assertEqual(v.x, 0)
            self.assertEqual(v.y, 0)

    def testInitializingConstructor(self):
        for Vec2x in Vec2Types:
            v = Vec2x(12.5, 42)
            self.assertEqual(v.x, 12.5)
            self.assertEqual(v.y, 42)

    def testFromTuple(self):
        for Vec2x in Vec2Types:
            t = (12.5, 42)
            v = Vec2x(t)
            self.assertEqual(v.x, 12.5)
            self.assertEqual(v.y, 42)

            t2 = (12.5, 42, 12)
            with self.assertRaises(ValueError):
                v = Vec2x(t2)

    def testCopyByReference(self):
        for Vec2x in Vec2Types:
            v1 = Vec2x(12.5, 42)
            v2 = v1
            self.assertIs(v1, v2)
            self.assertEqual(v1, v2)
            v2.x = 15
            self.assertEqual(v1.x, 15)
            self.assertEqual(v1, v2)

    def testCopyByValue(self):
        for Vec2x in Vec2Types:
            v1 = Vec2x(12.5, 42)
            v2 = Vec2x(v1)
            self.assertIsNot(v1, v2)
            self.assertEqual(v1, v2)
            v2.x = 15
            self.assertEqual(v1.x, 12.5)
            self.assertNotEqual(v1, v2)

    def testBracketOperator(self):
        for Vec2x in Vec2Types:
            v = Vec2x(12.5, 42)
            self.assertEqual(v[0], 12.5)
            self.assertEqual(v[1], 42)
            v[0] = 13.5
            v[1] += 1
            self.assertEqual(v[0], 13.5)
            self.assertEqual(v[1], 43)

    def testXY(self):
        for Vec2x in Vec2Types:
            v = Vec2x(12.5, 42)
            self.assertEqual(v.x, 12.5)
            self.assertEqual(v.y, 42)
            v.x = 13.5
            v.y += 1
            self.assertEqual(v.x, 13.5)
            self.assertEqual(v.y, 43)

    def testArithmeticOperators(self):
        for Vec2x in Vec2Types:
            v1 = Vec2x(1, 2)
            v1 += Vec2x(3, 4)
            self.assertEqual(v1.x, 4)
            self.assertEqual(v1.y, 6)
            self.assertEqual(v1, Vec2x(4, 6))
            v2 = v1 + Vec2x(1, 1)
            self.assertEqual(v1, Vec2x(4, 6))
            self.assertEqual(v2, Vec2x(5, 7))
            v3 = +v2
            self.assertEqual(v2, Vec2x(5, 7))
            self.assertEqual(v3, Vec2x(5, 7))
            v3 = +v3
            self.assertEqual(v3, Vec2x(5, 7))
            v2 -= Vec2x(3, 2)
            self.assertEqual(v2, Vec2x(2, 5))
            v1 = v1 - v2
            self.assertEqual(v1, Vec2x(2, 1))
            v3 = - v2
            self.assertEqual(v2, Vec2x(2, 5))
            self.assertEqual(v3, Vec2x(-2, -5))
            v3 = - v3
            self.assertEqual(v3, Vec2x(2, 5))
            v1 *= 2
            self.assertEqual(v1, Vec2x(4, 2))
            v3 = 3 * v1 * 2
            self.assertEqual(v3, Vec2x(24, 12))
            v3 /= 2
            self.assertEqual(v3, Vec2x(12, 6))
            v4 = v3 / 12
            self.assertEqual(v4, Vec2x(1, 0.5))

    def testComparisonOperators(self):
        for Vec2x in Vec2Types:
            v1 = Vec2x(1, 2)
            v2 = Vec2x(3, 4)
            self.assertTrue(v1 == v1)
            self.assertTrue(v1 == Vec2x(1, 2))
            self.assertTrue(v1 != v2)
            self.assertTrue(v1 != Vec2x(3, 4))
            self.assertTrue(v1 < v2)
            self.assertTrue(v1 < Vec2x(2, 0))
            self.assertTrue(v1 < Vec2x(1, 3))
            self.assertTrue(v1 <= v1)
            self.assertTrue(v1 <= v2)
            self.assertTrue(v1 <= Vec2x(2, 0))
            self.assertTrue(v1 <= Vec2x(1, 3))
            self.assertTrue(v2 > v1)
            self.assertTrue(v2 > Vec2x(2, 100))
            self.assertTrue(v2 >= v2)
            self.assertTrue(v2 >= v1)
            self.assertTrue(v2 >= Vec2x(2, 100))

    def testLength(self):
        for Vec2x in Vec2Types:
            for v in [Vec2x(3, 4), Vec2x(-3, 4), Vec2x(3, -4), Vec2x(-3, -4)]:
                self.assertEqual(v.length(), 5)
                self.assertEqual(v.squaredLength(), 25)

    def testNormalize(self):
        for Vec2x in Vec2Types:
            v = Vec2x(3, 4)
            v.normalize()
            self.assertEqual(v.length(), 1)
            self.assertEqual(v, Vec2x(0.6, 0.8))

    def testNormalized(self):
        for Vec2x in Vec2Types:
            v1 = Vec2x(3, 4)
            v2 = v1.normalized()
            self.assertEqual(v2.length(), 1)
            self.assertEqual(v1, Vec2x(3, 4))
            self.assertEqual(v2, Vec2x(0.6, 0.8))

    def testOrthogonalize(self):
        for Vec2x in Vec2Types:
            v = Vec2x(3, 4)
            v.orthogonalize()
            self.assertEqual(v, Vec2x(-4, 3))

    def testOrthogonalized(self):
        for Vec2x in Vec2Types:
            v1 = Vec2x(3, 4)
            v2 = v1.orthogonalized()
            self.assertEqual(v1, Vec2x(3, 4))
            self.assertEqual(v2, Vec2x(-4, 3))

    def testDot(self):
        for Vec2x in Vec2Types:
            v1 = Vec2x(1, 2)
            v2 = Vec2x(3, 4)
            self.assertEqual(v1.dot(v1), 5)
            self.assertEqual(v1.dot(v2), 11)

    def testDet(self):
        for Vec2x in Vec2Types:
            v1 = Vec2x(1, 2)
            v2 = Vec2x(3, 4)
            self.assertEqual(v1.det(v1), 0)
            self.assertEqual(v1.det(v2), -2)

    def testAngle(self):
        for Vec2x in Vec2Types:
            if Vec2x == Vec2d:
                places = 10
            else:
                places = 6
            v1 = Vec2x(1, 0)
            v2 = Vec2x(1, 1)
            v3 = Vec2x(-3, 0)
            v4 = Vec2x(-2, -2)
            self.assertEqual(v1.angle(v1), 0)
            self.assertAlmostEqual(v1.angle(v2), pi/4, places=places)
            self.assertAlmostEqual(v1.angle(v3), pi, places=places)
            self.assertAlmostEqual(v1.angle(v4), -3*pi/4, places=places)
            self.assertAlmostEqual(v2.angle(v4), pi, places=places)
            self.assertAlmostEqual(v4.angle(v3), -pi/4, places=places)

    def testParse(self):
        for Vec2x in Vec2Types:
            v = Vec2x("(1, 2.5)")
            self.assertTrue(v == Vec2x(1, 2.5))

    def testIsClose(self):
        for Vec2x in Vec2Types:
            self.assertTrue(Vec2x(0.0, 0.0).isClose(Vec2x(0.0, 0.0)))
            self.assertTrue(Vec2x(0.0, 42.0).isClose(Vec2x(0.0, 42.0)))
            self.assertTrue(Vec2x(42.0, 0.0).isClose(Vec2x(42.0, 0.0)))
            self.assertTrue(Vec2x(42.0, 42.0).isClose(Vec2x(42.0, 42.0)))
            self.assertTrue(Vec2x(1.03, 2.5).isClose(Vec2x(1.03, 2.5)))
            self.assertTrue(Vec2x(1.03, 2.5).isClose(Vec2x(1.03, 2.5000000001)))
            self.assertTrue(Vec2x(1.03, 2.5).isClose(Vec2x(1.0300000000001, 2.5)))
            self.assertTrue(Vec2x(1.03, 2.5).isClose(Vec2x(1.0300000000001, 2.5000000001)))
            self.assertFalse(Vec2x(1.03, 2.5).isClose(Vec2x(1.04, 2.5)))
            self.assertFalse(Vec2x(1.03, 2.5).isClose(Vec2x(1.03, 2.6)))
            self.assertFalse(Vec2x(1.03, 2.5).isClose(Vec2x(1.04, 2.6)))
            self.assertTrue(Vec2x(1.03, 2.5).isClose(Vec2x(1.04, 2.6), 0.1))
            self.assertTrue(Vec2x(1.0, 0.0).isClose(Vec2x(1.0, 1e-10)))
            self.assertTrue(Vec2x( inf,  inf).isClose(Vec2x( inf,  inf)))
            self.assertTrue(Vec2x(-inf,  inf).isClose(Vec2x(-inf,  inf)))
            self.assertTrue(Vec2x( inf, -inf).isClose(Vec2x( inf, -inf)))
            self.assertTrue(Vec2x(-inf, -inf).isClose(Vec2x(-inf, -inf)))
            self.assertFalse(Vec2x( inf,  inf).isClose(Vec2x(-inf,  inf)))
            self.assertFalse(Vec2x( inf,  inf).isClose(Vec2x( inf, -inf)))
            self.assertFalse(Vec2x( inf,  inf).isClose(Vec2x(-inf, -inf)))
            self.assertFalse(Vec2x(-inf,  inf).isClose(Vec2x( inf,  inf)))
            self.assertFalse(Vec2x(-inf,  inf).isClose(Vec2x( inf, -inf)))
            self.assertFalse(Vec2x(-inf,  inf).isClose(Vec2x(-inf, -inf)))
            self.assertFalse(Vec2x( inf, -inf).isClose(Vec2x( inf,  inf)))
            self.assertFalse(Vec2x( inf, -inf).isClose(Vec2x(-inf,  inf)))
            self.assertFalse(Vec2x( inf, -inf).isClose(Vec2x(-inf, -inf)))
            self.assertFalse(Vec2x(-inf, -inf).isClose(Vec2x( inf,  inf)))
            self.assertFalse(Vec2x(-inf, -inf).isClose(Vec2x(-inf,  inf)))
            self.assertFalse(Vec2x(-inf, -inf).isClose(Vec2x( inf, -inf)))
            self.assertTrue(Vec2x(inf, 42.0).isClose(Vec2x(inf, 42.0)))
            self.assertTrue(Vec2x(inf, 42.0).isClose(Vec2x(inf, 42.0000000001)))
            self.assertTrue(Vec2x(inf, 42.0).isClose(Vec2x(inf, 43.0))) # (!)
            self.assertFalse(Vec2x(inf, 42.0).isClose(Vec2x(inf, inf)))

    def testAllClose(self):
        for Vec2x in Vec2Types:
            self.assertTrue(Vec2x(0.0, 0.0).allClose(Vec2x(0.0, 0.0)))
            self.assertTrue(Vec2x(0.0, 42.0).allClose(Vec2x(0.0, 42.0)))
            self.assertTrue(Vec2x(42.0, 0.0).allClose(Vec2x(42.0, 0.0)))
            self.assertTrue(Vec2x(42.0, 42.0).allClose(Vec2x(42.0, 42.0)))
            self.assertTrue(Vec2x(1.03, 2.5).allClose(Vec2x(1.03, 2.5)))
            self.assertTrue(Vec2x(1.03, 2.5).allClose(Vec2x(1.03, 2.5000000001)))
            self.assertTrue(Vec2x(1.03, 2.5).allClose(Vec2x(1.0300000000001, 2.5)))
            self.assertTrue(Vec2x(1.03, 2.5).allClose(Vec2x(1.0300000000001, 2.5000000001)))
            self.assertFalse(Vec2x(1.03, 2.5).allClose(Vec2x(1.04, 2.5)))
            self.assertFalse(Vec2x(1.03, 2.5).allClose(Vec2x(1.03, 2.6)))
            self.assertFalse(Vec2x(1.03, 2.5).allClose(Vec2x(1.04, 2.6)))
            self.assertTrue(Vec2x(1.03, 2.5).allClose(Vec2x(1.04, 2.6), 0.1))
            self.assertFalse(Vec2x(1.0, 0.0).allClose(Vec2x(1.0, 1e-10)))
            self.assertFalse(Vec2x(1.0, 0.0).allClose(Vec2x(1.0, 1e-10), 0.1))
            self.assertFalse(Vec2x(1.0, 0.0).allClose(Vec2x(1.0, 1e-10), 0.1, 1e-11))
            self.assertTrue(Vec2x(1.0, 0.0).allClose(Vec2x(1.0, 1e-10), 0.1, 1e-9))
            self.assertTrue(Vec2x( inf,  inf).allClose(Vec2x( inf,  inf)))
            self.assertTrue(Vec2x(-inf,  inf).allClose(Vec2x(-inf,  inf)))
            self.assertTrue(Vec2x( inf, -inf).allClose(Vec2x( inf, -inf)))
            self.assertTrue(Vec2x(-inf, -inf).allClose(Vec2x(-inf, -inf)))
            self.assertFalse(Vec2x( inf,  inf).allClose(Vec2x(-inf,  inf)))
            self.assertFalse(Vec2x( inf,  inf).allClose(Vec2x( inf, -inf)))
            self.assertFalse(Vec2x( inf,  inf).allClose(Vec2x(-inf, -inf)))
            self.assertFalse(Vec2x(-inf,  inf).allClose(Vec2x( inf,  inf)))
            self.assertFalse(Vec2x(-inf,  inf).allClose(Vec2x( inf, -inf)))
            self.assertFalse(Vec2x(-inf,  inf).allClose(Vec2x(-inf, -inf)))
            self.assertFalse(Vec2x( inf, -inf).allClose(Vec2x( inf,  inf)))
            self.assertFalse(Vec2x( inf, -inf).allClose(Vec2x(-inf,  inf)))
            self.assertFalse(Vec2x( inf, -inf).allClose(Vec2x(-inf, -inf)))
            self.assertFalse(Vec2x(-inf, -inf).allClose(Vec2x( inf,  inf)))
            self.assertFalse(Vec2x(-inf, -inf).allClose(Vec2x(-inf,  inf)))
            self.assertFalse(Vec2x(-inf, -inf).allClose(Vec2x( inf, -inf)))
            self.assertTrue(Vec2x(inf, 42.0).allClose(Vec2x(inf, 42.0)))
            self.assertTrue(Vec2x(inf, 42.0).allClose(Vec2x(inf, 42.0000000001)))
            self.assertFalse(Vec2x(inf, 42.0).allClose(Vec2x(inf, 43.0))) # (!)
            self.assertFalse(Vec2x(inf, 42.0).allClose(Vec2x(inf, inf)))

    def testIsNear(self):
        for Vec2x in Vec2Types:
            absTol = 0.001
            self.assertTrue(Vec2x(0.0, 0.0).isNear(Vec2x(0.0, 0.0), absTol))
            self.assertTrue(Vec2x(0.0, 42.0).isNear(Vec2x(0.0, 42.0), absTol))
            self.assertTrue(Vec2x(42.0, 0.0).isNear(Vec2x(42.0, 0.0), absTol))
            self.assertTrue(Vec2x(42.0, 42.0).isNear(Vec2x(42.0, 42.0), absTol))
            self.assertTrue(Vec2x(0.0, 0.0).isNear(Vec2x(0.0, 0.0), 0.0))
            self.assertTrue(Vec2x(0.0, 42.0).isNear(Vec2x(0.0, 42.0), 0.0))
            self.assertTrue(Vec2x(42.0, 0.0).isNear(Vec2x(42.0, 0.0), 0.0))
            self.assertTrue(Vec2x(42.0, 42.0).isNear(Vec2x(42.0, 42.0), 0.0))
            self.assertTrue(Vec2x(1.03, 2.5).isNear(Vec2x(1.03, 2.5), absTol))
            self.assertTrue(Vec2x(1.03, 2.5).isNear(Vec2x(1.03, 2.5000000001), absTol))
            self.assertTrue(Vec2x(1.03, 2.5).isNear(Vec2x(1.0300000000001, 2.5), absTol))
            self.assertTrue(Vec2x(1.03, 2.5).isNear(Vec2x(1.0300000000001, 2.5000000001), absTol))
            self.assertFalse(Vec2x(1.03, 2.5).isNear(Vec2x(1.04, 2.5), absTol))
            self.assertFalse(Vec2x(1.03, 2.5).isNear(Vec2x(1.03, 2.6), absTol))
            self.assertFalse(Vec2x(1.03, 2.5).isNear(Vec2x(1.04, 2.6), absTol))
            self.assertFalse(Vec2x(1.03, 2.5).isNear(Vec2x(1.04, 2.6), 0.1))
            self.assertTrue(Vec2x(1.03, 2.5).isNear(Vec2x(1.04, 2.6), 0.2))
            self.assertTrue(Vec2x(1.0, 0.0).isNear(Vec2x(1.0, 1e-10), absTol))
            self.assertTrue(Vec2x(1.0, 0.0).isNear(Vec2x(1.0, 1e-10), 0.1))
            self.assertFalse(Vec2x(1.0, 0.0).isNear(Vec2x(1.0, 1e-10), 1e-11))
            self.assertTrue(Vec2x(1.0, 0.0).isNear(Vec2x(1.0, 1e-10), 1e-9))
            self.assertTrue(Vec2x( inf,  inf).isNear(Vec2x( inf,  inf), absTol))
            self.assertTrue(Vec2x(-inf,  inf).isNear(Vec2x(-inf,  inf), absTol))
            self.assertTrue(Vec2x( inf, -inf).isNear(Vec2x( inf, -inf), absTol))
            self.assertTrue(Vec2x(-inf, -inf).isNear(Vec2x(-inf, -inf), absTol))
            self.assertFalse(Vec2x( inf,  inf).isNear(Vec2x(-inf,  inf), absTol))
            self.assertFalse(Vec2x( inf,  inf).isNear(Vec2x( inf, -inf), absTol))
            self.assertFalse(Vec2x( inf,  inf).isNear(Vec2x(-inf, -inf), absTol))
            self.assertFalse(Vec2x(-inf,  inf).isNear(Vec2x( inf,  inf), absTol))
            self.assertFalse(Vec2x(-inf,  inf).isNear(Vec2x( inf, -inf), absTol))
            self.assertFalse(Vec2x(-inf,  inf).isNear(Vec2x(-inf, -inf), absTol))
            self.assertFalse(Vec2x( inf, -inf).isNear(Vec2x( inf,  inf), absTol))
            self.assertFalse(Vec2x( inf, -inf).isNear(Vec2x(-inf,  inf), absTol))
            self.assertFalse(Vec2x( inf, -inf).isNear(Vec2x(-inf, -inf), absTol))
            self.assertFalse(Vec2x(-inf, -inf).isNear(Vec2x( inf,  inf), absTol))
            self.assertFalse(Vec2x(-inf, -inf).isNear(Vec2x(-inf,  inf), absTol))
            self.assertFalse(Vec2x(-inf, -inf).isNear(Vec2x( inf, -inf), absTol))
            self.assertTrue(Vec2x(inf, 42.0).isNear(Vec2x(inf, 42.0), absTol))
            self.assertTrue(Vec2x(inf, 42.0).isNear(Vec2x(inf, 42.0000000001), absTol))
            self.assertFalse(Vec2x(inf, 42.0).isNear(Vec2x(inf, 43.0), absTol)) # (!)
            self.assertFalse(Vec2x(inf, 42.0).isNear(Vec2x(inf, inf), absTol))

    def testAllNear(self):
        for Vec2x in Vec2Types:
            absTol = 0.001
            self.assertTrue(Vec2x(0.0, 0.0).allNear(Vec2x(0.0, 0.0), absTol))
            self.assertTrue(Vec2x(0.0, 42.0).allNear(Vec2x(0.0, 42.0), absTol))
            self.assertTrue(Vec2x(42.0, 0.0).allNear(Vec2x(42.0, 0.0), absTol))
            self.assertTrue(Vec2x(42.0, 42.0).allNear(Vec2x(42.0, 42.0), absTol))
            self.assertTrue(Vec2x(0.0, 0.0).allNear(Vec2x(0.0, 0.0), 0.0))
            self.assertTrue(Vec2x(0.0, 42.0).allNear(Vec2x(0.0, 42.0), 0.0))
            self.assertTrue(Vec2x(42.0, 0.0).allNear(Vec2x(42.0, 0.0), 0.0))
            self.assertTrue(Vec2x(42.0, 42.0).allNear(Vec2x(42.0, 42.0), 0.0))
            self.assertTrue(Vec2x(1.03, 2.5).allNear(Vec2x(1.03, 2.5), absTol))
            self.assertTrue(Vec2x(1.03, 2.5).allNear(Vec2x(1.03, 2.5000000001), absTol))
            self.assertTrue(Vec2x(1.03, 2.5).allNear(Vec2x(1.0300000000001, 2.5), absTol))
            self.assertTrue(Vec2x(1.03, 2.5).allNear(Vec2x(1.0300000000001, 2.5000000001), absTol))
            self.assertFalse(Vec2x(1.03, 2.5).allNear(Vec2x(1.04, 2.5), absTol))
            self.assertFalse(Vec2x(1.03, 2.5).allNear(Vec2x(1.03, 2.6), absTol))
            self.assertFalse(Vec2x(1.03, 2.5).allNear(Vec2x(1.04, 2.6), absTol))
            self.assertFalse(Vec2x(1.03, 2.5).allNear(Vec2x(1.04, 2.6), 0.09))
            self.assertTrue(Vec2x(1.03, 2.5).allNear(Vec2x(1.04, 2.6), 0.11))
            self.assertTrue(Vec2x(1.0, 0.0).allNear(Vec2x(1.0, 1e-10), absTol))
            self.assertTrue(Vec2x(1.0, 0.0).allNear(Vec2x(1.0, 1e-10), 0.1))
            self.assertFalse(Vec2x(1.0, 0.0).allNear(Vec2x(1.0, 1e-10), 1e-11))
            self.assertTrue(Vec2x(1.0, 0.0).allNear(Vec2x(1.0, 1e-10), 1e-9))
            self.assertTrue(Vec2x( inf,  inf).allNear(Vec2x( inf,  inf), absTol))
            self.assertTrue(Vec2x(-inf,  inf).allNear(Vec2x(-inf,  inf), absTol))
            self.assertTrue(Vec2x( inf, -inf).allNear(Vec2x( inf, -inf), absTol))
            self.assertTrue(Vec2x(-inf, -inf).allNear(Vec2x(-inf, -inf), absTol))
            self.assertFalse(Vec2x( inf,  inf).allNear(Vec2x(-inf,  inf), absTol))
            self.assertFalse(Vec2x( inf,  inf).allNear(Vec2x( inf, -inf), absTol))
            self.assertFalse(Vec2x( inf,  inf).allNear(Vec2x(-inf, -inf), absTol))
            self.assertFalse(Vec2x(-inf,  inf).allNear(Vec2x( inf,  inf), absTol))
            self.assertFalse(Vec2x(-inf,  inf).allNear(Vec2x( inf, -inf), absTol))
            self.assertFalse(Vec2x(-inf,  inf).allNear(Vec2x(-inf, -inf), absTol))
            self.assertFalse(Vec2x( inf, -inf).allNear(Vec2x( inf,  inf), absTol))
            self.assertFalse(Vec2x( inf, -inf).allNear(Vec2x(-inf,  inf), absTol))
            self.assertFalse(Vec2x( inf, -inf).allNear(Vec2x(-inf, -inf), absTol))
            self.assertFalse(Vec2x(-inf, -inf).allNear(Vec2x( inf,  inf), absTol))
            self.assertFalse(Vec2x(-inf, -inf).allNear(Vec2x(-inf,  inf), absTol))
            self.assertFalse(Vec2x(-inf, -inf).allNear(Vec2x( inf, -inf), absTol))
            self.assertTrue(Vec2x(inf, 42.0).allNear(Vec2x(inf, 42.0), absTol))
            self.assertTrue(Vec2x(inf, 42.0).allNear(Vec2x(inf, 42.0000000001), absTol))
            self.assertFalse(Vec2x(inf, 42.0).allNear(Vec2x(inf, 43.0), absTol)) # (!)
            self.assertFalse(Vec2x(inf, 42.0).allNear(Vec2x(inf, inf), absTol))

    def testToString(self):
        for Vec2x in Vec2Types:
            # Setup a French locale (if available on this system) to check that even
            # when the decimal point is ',' according to the locale, numbers are
            # still printed with '.' as decimal point.
            #
            try:
                locale.setlocale(locale.LC_ALL, 'fr_FR.UTF8')
            except:
                pass
            v = Vec2x(1, 2.5)
            self.assertEqual(str(v), "(1, 2.5)")


class TestVec2dArray(unittest.TestCase):

    def testDefaultConstructor(self):
        a = Vec2dArray()
        self.assertEqual(len(a), 0)

    def testInitializingConstructors(self):
        n = 3
        x0 = Vec2d(0.5, 0.7)

        a1 = Vec2dArray(n)
        self.assertEqual(len(a1), n)
        for x in a1:
            self.assertEqual(x, Vec2d(0, 0))

        a2 = Vec2dArray(n, x0)
        self.assertEqual(len(a2), n)
        for x in a2:
            self.assertEqual(x, x0)

        a3 = Vec2dArray([(1, 2), (3, 4)])
        self.assertEqual(len(a3), 2)
        self.assertEqual(a3[0], Vec2d(1, 2))
        self.assertEqual(a3[1], Vec2d(3, 4))

    def testAppend(self):
        a = Vec2dArray()
        a.append(Vec2d(1, 2))
        a.append(Vec2d(3, 4))
        self.assertEqual(a, Vec2dArray([(1, 2), (3, 4)]))

    def testParse(self):
        a = Vec2dArray("[(1, 2), (3, 4.5)]")
        self.assertTrue(a == Vec2dArray([(1, 2), (3, 4.5)]))
        a = Vec2dArray("[]")
        self.assertTrue(a == Vec2dArray())

    def testContains(self):
        a3 = Vec2dArray([(1, 2), (3, 4), (5, 6)])
        self.assertTrue(Vec2d(3, 4) in a3)
        self.assertTrue(a3.__contains__(Vec2d(3, 4)))
        self.assertFalse(Vec2d(4, 3) in a3)
        self.assertFalse(a3.__contains__(Vec2d(4, 3)))
        self.assertTrue(Vec2d(4, 3) not in a3)


if __name__ == '__main__':
    unittest.main()
