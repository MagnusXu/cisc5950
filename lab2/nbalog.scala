package com.cn.paic
import java.io.File
import java.lang.Math.{pow, sqrt}
import org.apache.spark.sql.SparkSession
import scala.annotation.tailrec
import scala.util.Random
import scala.collection.immutable.ListMap


class KMeansClustering {
	def initData(file_path:String): List = {
		val clusters = 4
		val lines = spark.read.textFile(file_path).rdd
		val data = lines.map(parseVector _).cache()
		var errors = lines.filter(_.startsWith("ERROR"))
		val messages = error.map(_.split("\t")).map(r => r(1))
		messages.cache()
		List(lines, data)
	}

	def initCentroids(k:Int, num:Int):Seq[Point] = {
		val randx = new Random(1)
		val randy = new Random(3)
		val randz = new Random(5)
		(0 until num)
		.map({i =>
			val x = ((i + 1) % k) * 1.0 / k + randx.nextDouble() * 0.5
			val y = ((i + 1) % k) * 1.0 / k + randy.nextDouble() * 0.5
			val z = ((i + 1) % k) * 1.0 / k + randz.nextDouble() * 0.5
		}).to[mutable.ArrayBuffer]
	}

	def initMeans(k: Int, points: Seq[Point]): Seq[Point] = {
        val rand = new Random(7)
        (0 until k).map(_ => points(rand.nextInt(points.length))).to[mutable.ArrayBuffer]
    }

    def closestPoint(p: Point, means: GenSeq[Point]): Point = {
        assert(means.size > 0)
        var minDistance = p.squareDistance(means(0))
        var closest = means(0)
        var i = 1
        while (i < means.length) {
            val distance = p.squareDistance(means(i))
            if (distance < minDistance) {
                minDistance = distance
                closest = means(i)
            }
            i += 1
        }
        closest
    }

    def validate(coords: List) {
    	if (coords[0] == 'SHOT_DIST')
    		false
    	for (x <- coords)
    		if (x == "")
    			false
    		else if (x.toFloat < 0)
    			false
    	true
    }

    def errorWarning() {
    	System.err.println(
    		"Error Warning".stripMargin
    	)
    }

    // First half to ensure all means are in the result even if some might have empty lists
    def classify(points: GenSeq[Point], means: GenSeq[Point]): GenMap[Point, GenSeq[Point]] = {
        means.map{(_, GenSeq())}.toMap ++ points.groupBy(findClosest(_, means))
    }

    def findAverage(oldMean: Point, points: GenSeq[Point]): Point = if (points.length == 0) oldMean else {
        var x = 0.0
        var y = 0.0
        var z = 0.0
        points.seq.foreach { p =>
            x += p.x
            y += p.y
            z += p.z
        }
        new Point(x / points.length, y / points.length, z / points.length)
    }

    def update(classified: GenMap[Point, GenSeq[Point]], oldMeans: GenSeq[Point]): GenSeq[Point] = {
        oldMeans.map(mean => findAverage(mean, classified(mean)))
    }

    def converged(eta: Double)(oldMeans: GenSeq[Point], newMeans: GenSeq[Point]): Boolean = {
        oldMeans.zip(newMeans).forall{case (om, nm) => om.squareDistance(nm) <= eta}
    }

    @tailrec
    final def kMeans(points: GenSeq[Point], means: GenSeq[Point], eta: Double): GenSeq[Point] = {
        val classified = classify(points, means)
        val newMeans = update(classified, means)
        if (converged(eta)(means, newMeans)) newMeans
        else kMeans(points, newMeans, eta)
    }
}

class Point(val x: Double, val y: Double, val z: Double) {
    private def square(v: Double): Double = v * v
    def squareDistance(that: Point): Double = {
        square(that.x - x)  + square(that.y - y) + square(that.z - z)
    }
    private def round(v: Double): Double = (v * 100).toInt / 100.0
    override def toString = s"(${round(x)}, ${round(y)}, ${round(z)})"
}


object KMeansRunner {

    val standardConfig = config(
        Key.exec.minWarmupRuns -> 20,
        Key.exec.maxWarmupRuns -> 40,
        Key.exec.benchRuns -> 25,
        Key.verbose -> true
    ) withWarmer(new Warmer.Default)

    def main(args: Array[String]) {
    	if (args.length < 3) {
    		System.err.println("Usage: KMeansClustering <file> <k> <convergeDist>")
    		System.exit(1)
    	}

    	errorWarning()

        val kMeans = new KMeansClustering()

        val players: List[String] = List("james harden", "lebron james", "chris paul", "stephen curry")

        val numPoints = kMeans.initData()
        val eta = 0.01
        val k = 4
        val points = kMeans.initCentroids(k, numPoints)
        val means = kMeans.initMeans(k, points)
        var player_map:Map[Char, Int] = Map()

        for (lines <- data)
        	var cluster_map:Map[Char, Float] = Map()
        	var player = map(_.split("\t")).map(r => r(1))
        	var cluster = map(_.split("\t")).map(r => r(2))
        	var made = map(_.split("\t")).map(r => r(3))
        	made = made.toInt
        	if player_map.contains(player)
        		cluster_map[cluster] = [made, 1.0]
        		player_map[player] = cluster_map
        	else
        		cluster_map = player_map[player]
        		var val:List = (cluster, [0, 0.0])
        		cluster_map[cluster] = [val[0] + made, val[1] + 1]
        		player_map[player] = cluster_map
        for ((k, v) <- player_map)
        	for (lines <- player_map)
        		v = v[0] / v[1]
        val rate:Float = ListMap(player_map.toSeq.sortWith(_._2 > _._2):*)
        for ((k, v) <- player_map)
        	println("key: %s, value: %s\n", $k, $v)

        
    }
}
