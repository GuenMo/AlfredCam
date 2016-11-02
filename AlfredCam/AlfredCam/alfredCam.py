# coding:utf-8

import pymel.all as pm
import textwrap

class TumbleCamera(object):
    
    def __init__(self):
        self.camera      = None
        self.ctrl        = None
        self.expression  = None
        self.metaNode    = None
        self.extNode     = []
        
        if pm.ls(sl=True):
            self.getRigNode()
        else:
            pass
        
    def create(self, name):
        # Create and return camera.
        camera=pm.camera(
                        filmFit='Horizontal', 
                        horizontalPan=0, 
                        shutterAngle=144, 
                        verticalPan=0, 
                        horizontalFilmOffset=0, 
                        focalLength=35, 
                        centerOfInterest=5, 
                        motionBlur=0, 
                        horizontalFilmAperture=1.77777, 
                        overscan=1, 
                        panZoomEnabled=0, 
                        nearClipPlane=0.1, 
                        farClipPlane=10000, 
                        orthographic=0, 
                        verticalFilmOffset=0, 
                        verticalFilmAperture=1.0, 
                        lensSqueezeRatio=1, 
                        orthographicWidth=30, 
                        cameraScale=1, 
                        zoom=1)
        camera[0].rename(name)
        self.camera = camera[0]
        return camera
    
    def find(self, name):
        return pm.objExists(name)
            
    def createCtrl(self, name):
        #cameraName = camera[0].name()
        cameraShape = self.camera.getShape()
        
        # 그룹 리깅
        constraint     = pm.group(n=name + "_constraint", em=True)
        offset         = pm.group(n=name + "_offset")
        shakeTransform = pm.group(n=name + "_Shake")
        offsetTz       = pm.group(n=name + "_offsetTz")
        offsetTy       = pm.group(n=name + "_offsetTy")
        offsetTx       = pm.group(n=name + "_offsetTx")
        tz             = pm.group(n=name + "_tz")
        rz             = pm.group(n=name + "_rz")
        rx             = pm.group(n=name + "_rx")
        ry             = pm.group(n=name + "_ry")
        ctrl           = pm.group(n=name + "_Ctrl")
        pm.setAttr(ctrl + ".displayHandle",   1)
        pm.setAttr(ctrl + ".overrideEnabled", 1)
        pm.setAttr(ctrl + ".overrideColor",   7)#dark_green
        
        # Display
        dispGrp = pm.group(n=name + "_Template_Grp" , em=1)
        pm.parent(dispGrp, ctrl)
        pm.setAttr(dispGrp + ".overrideEnabled", 1)
        pm.setAttr(dispGrp + ".overrideDisplayType", 1)
        pm.setAttr(dispGrp + ".overrideColor", 7) #dark_green
    
        dispNodeList = []
        dispNodeList.extend(self.displayConnect([ctrl, tz]))
        dispNodeList.extend(self.displayConnect([tz, offsetTx]))
        dispNodeList.extend(self.displayConnect([offsetTx, offsetTy]))
        dispNodeList.extend(self.displayConnect([offsetTy, offsetTz]))
        
        # Outline
        for dispNode in dispNodeList:
            dispNode.rename(name + '_' + dispNode.name())
         
        pm.parent(dispNodeList, dispGrp)
        
        # Add attribute
        # Camera attribute
        pm.addAttr(ctrl, ln="Camera", en="Option:", at="enum")
        pm.setAttr(ctrl + ".Camera", e=1, channelBox=True)
        pm.addAttr(ctrl, ln="focalLength", dv=35, at='double', nn="FocalLength (mm)", keyable=True)
        pm.addAttr(ctrl, ln="overscan", dv=1, at='double', nn="Overscan", keyable=True)
        pm.addAttr(ctrl, ln="frameRange", at='double2', nn="Frame Range (frame)")
        pm.addAttr(ctrl, ln="startFrame", p='frameRange', at='double', nn="Start Frame", keyable=True)
        pm.addAttr(ctrl, ln="endFrame", p='frameRange', at='double', nn="End Frame", keyable=True)
        # Tumble attribute
        pm.addAttr(ctrl, ln="Tumble", en="Option:", at="enum")
        pm.setAttr(ctrl + ".Tumble", e=1, channelBox=True)
        pm.addAttr(ctrl, ln="tumbleTranslateZ", at='double', nn="Tumble Translate Z", keyable=True)
        pm.addAttr(ctrl, ln="tumbleRotate", at='double3', nn="Tumble Rotate")
        pm.addAttr(ctrl, ln="tumbleRotateX", p='tumbleRotate', at='double', nn="Tumble Rotate X", keyable=True)
        pm.addAttr(ctrl, ln="tumbleRotateY", p='tumbleRotate', at='double', nn="Tumble Rotate Y", keyable=True)
        pm.addAttr(ctrl, ln="tumbleRotateZ", p='tumbleRotate', at='double', nn="Tumble Rotate Z", keyable=True)
        # Shake attribute
        pm.addAttr(ctrl, ln="Shake", en="Option:", at="enum")
        pm.setAttr(ctrl + ".Shake", e=1, channelBox=True)
        pm.addAttr(ctrl, ln="time", keyable=False, at='double', nn="Shake Time (second)")
        pm.addAttr(ctrl, ln="timeOffset", keyable=False, at='double', nn="Shake Time Offset (second)")
        pm.addAttr(ctrl, ln="shake1", at='double2', nn=u"Shake 1st (진폭, 주기)")
        pm.addAttr(ctrl, ln="shakeAmplitude1", p='shake1', at='double', nn=u"Shake 1st (진폭)", keyable=True)
        pm.addAttr(ctrl, ln="shakeFrequency1", p='shake1', at='double', nn=u"Frequency 1st (주기)", keyable=True)
        pm.addAttr(ctrl, ln="noise1", at='double3', nn="Shake Noise 1st")
        pm.addAttr(ctrl, ln="noise1X", p='noise1', at='double', nn="Shake Noise 1 X")
        pm.addAttr(ctrl, ln="noise1Y", p='noise1', at='double', nn="Shake Noise 1 Y")
        pm.addAttr(ctrl, ln="noise1Z", p='noise1', at='double', nn="Shake Noise 1 Z")
        pm.addAttr(ctrl, ln="shake2", at='double2', nn=u"Shake 2nd (진폭, 주기)")
        pm.addAttr(ctrl, ln="shakeAmplitude2", p='shake2', at='double', nn=u"Shake 2nd (진폭)", keyable=True)
        pm.addAttr(ctrl, ln="shakeFrequency2", p='shake2', at='double', nn=u"Frequency 2nd (주기)", keyable=True)
        pm.addAttr(ctrl, ln="noise2", at='double3', nn="Shake Noise 2nd")
        pm.addAttr(ctrl, ln="noise2X", p='noise2', at='double', nn="Shake Noise 2 X")
        pm.addAttr(ctrl, ln="noise2Y", p='noise2', at='double', nn="Shake Noise 2 Y")
        pm.addAttr(ctrl, ln="noise2Z", p='noise2', at='double', nn="Shake Noise 2 Z")
        pm.addAttr(ctrl, ln="shakeTranslate", at='double3', nn="Shake Translate")
        pm.addAttr(ctrl, ln="shakeTranslateX", p='shakeTranslate', at='double', nn="Shake Translate X", keyable=True)
        pm.addAttr(ctrl, ln="shakeTranslateY", p='shakeTranslate', at='double', nn="Shake Translate Y", keyable=True)
        pm.addAttr(ctrl, ln="shakeTranslateZ", p='shakeTranslate', at='double', nn="Shake Translate Z", keyable=True)
        pm.addAttr(ctrl, ln="shakeRotate", at='double3', nn="Shake Rotate")
        pm.addAttr(ctrl, ln="shakeRotateX", p='shakeRotate', at='double', nn="Shake Rotate X", keyable=True)
        pm.addAttr(ctrl, ln="shakeRotateY", p='shakeRotate', at='double', nn="Shake Rotate Y", keyable=True)
        pm.addAttr(ctrl, ln="shakeRotateZ", p='shakeRotate', at='double', nn="Shake Rotate Z", keyable=True)
        pm.addAttr(ctrl, ln="shakeScale", at='double', dv=1.0, keyable=True)
        pm.addAttr(ctrl, ln="timeScale", at='double', dv=1.0, keyable=True)
        # Offset attribute
        pm.addAttr(ctrl, ln="Offset", en="Option:", at="enum")
        pm.setAttr(ctrl + ".Offset", e=1, channelBox=True)
        pm.addAttr(ctrl, ln="offsetTranslate", at='double3', nn="Offset Translate")
        pm.addAttr(ctrl, ln="offsetTranslateX", p='offsetTranslate', at='double', nn="Offset Translate X", keyable=True)
        pm.addAttr(ctrl, ln="offsetTranslateY", p='offsetTranslate', at='double', nn="Offset Translate Y", keyable=True)
        pm.addAttr(ctrl, ln="offsetTranslateZ", p='offsetTranslate', at='double', nn="Offset Translate Z", keyable=True)
        pm.addAttr(ctrl, ln="offsetRotate", at='double3', nn="Offset Rotate")
        pm.addAttr(ctrl, ln="offsetRotateX", p='offsetRotate', at='double', nn="Offset Rotate X", keyable=True)
        pm.addAttr(ctrl, ln="offsetRotateY", p='offsetRotate', at='double', nn="Offset Rotate Y", keyable=True)
        pm.addAttr(ctrl, ln="offsetRotateZ", p='offsetRotate', at='double', nn="Offset Rotate Z", keyable=True)
        # Display attribute
        pm.addAttr(ctrl, ln="Display", en="Option:", at="enum")
        pm.setAttr(ctrl + ".Display", e=1, channelBox=True)
        pm.addAttr(ctrl, ln="cameraScale", dv=1, at='double', nn="Camera Scale", keyable=True)
        pm.addAttr(ctrl, en="off:on:", nn="Display Ctrler", ln="displayCtrler", keyable=1, at="enum", dv=1)
        
        # Connect Attr
        pm.connectAttr(ctrl + ".cameraScale",       name + ".sx")
        pm.connectAttr(ctrl + ".cameraScale",       name + ".sy")
        pm.connectAttr(ctrl + ".cameraScale",       name + ".sz")
        pm.connectAttr(ctrl + ".focalLength",       cameraShape + ".focalLength")
        pm.connectAttr(ctrl + ".overscan",          cameraShape + ".overscan")
        pm.connectAttr(ctrl + ".tumbleRotateX",     rx + ".rx")
        pm.connectAttr(ctrl + ".tumbleRotateY",     ry + ".ry")
        pm.connectAttr(ctrl + ".tumbleRotateZ",     rz + ".rz")
        pm.connectAttr(ctrl + ".tumbleTranslateZ",  tz + ".tz")
        pm.connectAttr(ctrl + ".offsetTranslateX",  offsetTx + ".tx")
        pm.connectAttr(ctrl + ".offsetTranslateY",  offsetTy + ".ty")
        pm.connectAttr(ctrl + ".offsetTranslateZ",  offsetTz + ".tz")
        pm.connectAttr(ctrl + ".offsetRotate",      offset + ".r")
        pm.connectAttr(ctrl + ".displayCtrler",     dispGrp + ".v")
        
        # Lock and Hide unused attr
        attrList = ["_ry.tx", "_ry.ty", "_ry.tz", "_ry.rx", "_ry.rz", "_ry.sx", "_ry.sy", "_ry.sz", "_ry.v",  
                    "_rx.tx", "_rx.ty", "_rx.tz", "_rx.ry", "_rx.rz", "_rx.sx", "_rx.sy", "_rx.sz", "_rx.v",  
                    "_rz.tx", "_rz.ty", "_rz.tz", "_rz.rx", "_rz.ry", "_rz.sx", "_rz.sy", "_rz.sz", "_rz.v",  
                    "_tz.tx", "_tz.ty", "_tz.rx", "_tz.ry", "_tz.rz", "_tz.sx", "_tz.sy", "_tz.sz", "_tz.v",  
                    "_offsetTx.ty", "_offsetTx.tz", "_offsetTx.rx", "_offsetTx.ry", "_offsetTx.rz", "_offsetTx.sx", "_offsetTx.sy", "_offsetTx.sz", "_offsetTx.v",  
                    "_offsetTy.tx", "_offsetTy.tz", "_offsetTy.rx", "_offsetTy.ry", "_offsetTy.rz", "_offsetTy.sx", "_offsetTy.sy", "_offsetTy.sz", "_offsetTy.v",  
                    "_offsetTz.tx", "_offsetTz.ty", "_offsetTz.rx", "_offsetTz.ry", "_offsetTz.rz", "_offsetTz.sx", "_offsetTz.sy", "_offsetTz.sz", "_offsetTz.v",  
                    "_offset.sx", "_offset.sy", "_offset.sz", "_offset.v",
                    "_Ctrl.sx", "_Ctrl.sy", "_Ctrl.sz"]
    
        for attr in attrList:
            pm.setAttr(name + attr, lock=True, channelBox=False, keyable=False)
        pm.setAttr(cameraShape + ".orthographic",       lock=False, channelBox=False, keyable=True)
        pm.setAttr(cameraShape + ".orthographicWidth",  lock=False, channelBox=False, keyable=True)
        
        # Constraint camera
        const = pm.parentConstraint(constraint, self.camera, n=name+'_parentConstraint')
        pm.setAttr(const + ".nds", lock=True, channelBox=False, keyable=False)
        pm.setAttr(const + ".int", lock=True, channelBox=False, keyable=False)
        pm.setAttr(const + ".w0",  lock=True, channelBox=False, keyable=False)
        pm.parent(const, ctrl)
        
        # Add and Connect message
        attr="camera"
        nodes = [self.camera, ctrl]
        for node in nodes:
            if node.hasAttr(attr):
                node.deleteAttr(attr)
            pm.addAttr(node, ln=attr, multi=1, attributeType="message", indexMatters=False)
        
        for node in nodes:
            for i in range(0,2):
                pm.connectAttr('{}.message'.format(nodes[i].name()), '{}.{}[{}]'.format( node.name(), attr, str(i)), f=1)
      
        # Return
        self.ctrl = ctrl 
        uitConvertsion = self.ctrl.outputs(type="unitConversion")
        for uit in uitConvertsion:
            pm.rename(uit.name(), name+'_'+ uit.name())
        
        del self.extNode[:]
        self.extNode.extend([constraint, offset, shakeTransform, offsetTz, offsetTy, offsetTx, tz, rz, rx, ry, ctrl])
        self.extNode.extend(dispNodeList)
        self.extNode.extend(uitConvertsion)
        pm.select(self.ctrl, r=1)
        return ctrl
    
    def matchFilmBackToResolution(self, cameraShape):
        renderGlobal = pm.PyNode('defaultResolution')
        width        = float(renderGlobal.width.get())
        height       = float(renderGlobal.height.get())
        pm.setAttr(cameraShape + ".horizontalFilmAperture", (width / height))
        pm.setAttr(cameraShape + ".verticalFilmAperture", 1)
        
    def setCameraForBig(self, ctrl, cameraShape):
        pm.setAttr(ctrl + ".cameraScale", 10)
        pm.setAttr(cameraShape + ".nearClipPlane", 1)
        pm.setAttr(cameraShape + ".farClipPlane", 100000)
        pm.setAttr(cameraShape + ".displayResolution", 1)
        
    def displayConnect(self, obj):
        # Create curve for display, between selected objects
        # Return [curve, locator1, locator2]
        if len(obj) == 0:
            obj=pm.ls(transforms=1, sl=1)
            
        if len(obj)<2:
            pm.error(u"KH_curve_Connect : 선택된 오브젝트가 없습니다.")
            
        pointA=obj[0]
        pointB=obj[1]
    
        curve = pm.curve(p=[(0, 0, 0), (0, 0, 0)], k=[0, 1], d=1)
        pointCurveConstraint1 = pm.pointCurveConstraint(curve + ".ep[0]", ch=True)
        pointCurveConstraint2 = pm.pointCurveConstraint(curve + ".ep[1]", ch=True)
    
        pointCostraint1 = pm.pointConstraint(pointA, pointCurveConstraint1[0])
        pointCostraint2 = pm.pointConstraint(pointB, pointCurveConstraint2[0])
        
        locShape1=pm.listRelatives(pointCurveConstraint1[0], s=1)
        locShape2=pm.listRelatives(pointCurveConstraint2[0], s=1)
        pm.setAttr(locShape1[0] + ".visibility", 0)
        pm.setAttr(locShape2[0] + ".visibility", 0)
    
        return [curve, pm.PyNode(pointCurveConstraint1[0]), pm.PyNode(pointCurveConstraint2[0]), pointCostraint1, pointCostraint2]    
    
    def setPlaybackRange_ofCamera(self,camera):
        if not camera.hasAttr("frameRange"):
            return 
        pm.playbackOptions(min=camera.startFrame, max=camera.endFrame, ast=camera.startFrame, aet=camera.endFrame)

    def setDefault(self, ctrl):
        # Camera
        ctrl.focalLength.set(35.0)
        ctrl.overscan.set(1)
        ctrl.startFrame.set(pm.playbackOptions(q=True, min=True))
        ctrl.endFrame.set(pm.playbackOptions(q=True, max=True))
        # Tumble
        ctrl.tumbleTranslateZ.set(24)
        ctrl.tumbleRotateX.set(-30)
        ctrl.tumbleRotateY.set(45)
        ctrl.tumbleRotateZ.set(0)
        # Shake
        ctrl.timeOffset.set(3)
        ctrl.shakeAmplitude1.set(3)
        ctrl.shakeFrequency1.set(0.8)
        ctrl.shakeAmplitude2.set(0)
        ctrl.shakeFrequency2.set(10)
        ctrl.shakeTranslateX.set(0.2)
        ctrl.shakeTranslateY.set(0.2)
        ctrl.shakeTranslateZ.set(0.2)
        ctrl.shakeRotateX.set(1)
        ctrl.shakeRotateY.set(1)
        ctrl.shakeRotateZ.set(1)

    def createExpression(self, camera, ctrl):
        shakeTransform = camera.name() +'_Shake'
        exp = '''
        {ctrl}.time = time;\n
        float $time   = {ctrl}.time;
        float $timeScale = {ctrl}.timeScale;
        $time = $time * $timeScale;
        float $offset = {ctrl}.timeOffset;
        float $ampl1  = {ctrl}.shakeAmplitude1;
        float $freq1  = {ctrl}.shakeFrequency1;
        float $ampl2  = {ctrl}.shakeAmplitude2;
        float $freq2  = {ctrl}.shakeFrequency2;
        float $shakeTrX = {ctrl}.shakeTranslateX;
        float $shakeTrY = {ctrl}.shakeTranslateY;
        float $shakeTrZ = {ctrl}.shakeTranslateZ;
        float $shakeRtX = {ctrl}.shakeRotateX;
        float $shakeRtY = {ctrl}.shakeRotateY;
        float $shakeRtZ = {ctrl}.shakeRotateZ;
        float $noise1X = {ctrl}.noise1X = noise( ($time + $offset * 1) * $freq1 ) * $ampl1;
        float $noise1Y = {ctrl}.noise1Y = noise( ($time + $offset * 2) * $freq1 ) * $ampl1;
        float $noise1Z = {ctrl}.noise1Z = noise( ($time + $offset * 3) * $freq1 ) * $ampl1;
        float $noise2X = {ctrl}.noise2X = noise( ($time + $offset * 1) * $freq2 ) * $ampl2;
        float $noise2Y = {ctrl}.noise2Y = noise( ($time + $offset * 2) * $freq2 ) * $ampl2;
        float $noise2Z = {ctrl}.noise2Z = noise( ($time + $offset * 3) * $freq2 ) * $ampl2;
        float $shakeScale = {ctrl}.shakeScale;\n
        {shakeTransform}.tx = ($noise1X + $noise2X) * $shakeTrX * $shakeScale;
        {shakeTransform}.ty = ($noise1Y + $noise2Y) * $shakeTrY * $shakeScale;
        {shakeTransform}.tz = ($noise1Z + $noise2Z) * $shakeTrZ * $shakeScale;
        {shakeTransform}.rx = ($noise1X + $noise2X) * $shakeRtX * $shakeScale;
        {shakeTransform}.ry = ($noise1Y + $noise2Y) * $shakeRtY * $shakeScale;
        {shakeTransform}.rz = ($noise1Z + $noise2Z) * $shakeRtZ * $shakeScale;
        '''.format(ctrl=ctrl, shakeTransform=shakeTransform)
        exp = textwrap.dedent(exp)
        expressionNode = pm.expression(s=exp, ae=1, uc='all', o=ctrl, n=(camera + "_Expression"))
        self.expression = expressionNode
        uitConvertsion = expressionNode.outputs(type="unitConversion")
        for uit in uitConvertsion:
            pm.rename(uit.name(), self.camera.name()+'_'+ uit.name())
        self.extNode.extend(uitConvertsion)
        return expressionNode
    
    def lockNodes(self):
        for node in self.getRigNode().inputs():
            pm.lockNode(node)
        rigNode = self.getRigNode()
        pm.select(rigNode.ctrl.get())
    
    def unlockNodes(self):
        for node in self.getRigNode().inputs():
            pm.lockNode(node, lock=False)
        rigNode = self.getRigNode()
        pm.select(rigNode.ctrl.get())
    
    def createMeta(self, name):
        metaNode = pm.createNode('network', n= name + '_RigNode')
        
        # create system info
        metaNode.addAttr('cameraRigInfo', numberOfChildren=5, attributeType='compound' )
        metaNode.addAttr('Class',       dt='string',  parent='cameraRigInfo')
        metaNode.addAttr('camera',      at='message', parent='cameraRigInfo')
        metaNode.addAttr('ctrl',        at='message', parent='cameraRigInfo')
        metaNode.addAttr('expression',  at='message', parent='cameraRigInfo')
        metaNode.addAttr('ext', m=True, at='message', parent='cameraRigInfo')
        metaNode.Class.set('TumbleCamera')
        metaNode.Class.lock()
        self.metaNode = metaNode
        self.connectMeta(metaNode)
        
    def connectMeta(self, metaNode):
        self.camera.message.connect(metaNode.camera)
        self.ctrl.message.connect(metaNode.ctrl)
        self.expression.message.connect(metaNode.expression)
        
        i = 0
        for ext in self.extNode:
            ext.message.connect(metaNode.ext[i])
            i += 1
        pm.select(self.ctrl, r=1)
        
    def isTumbleCamera(self, node):
        if node.message.isConnected():
            for n in node.message.outputs(type='network'):
                if n.hasAttr('Class') and n.Class.get() == 'TumbleCamera':
                    return True
                else:
                    return False
        else:
            return False
        
    def getRigNode(self):
        node = pm.ls(sl=True)[0]
        if node.message.isConnected():
            for n in node.message.outputs(type='network'):
                return n
                
    def getCtrl(self):
        rigNode = self.getRigNode()
        return rigNode.ctrl.get()
    
    def getCameraShape(self):
        rigNode = self.getRigNode()
        camera = rigNode.camera.get()
        cameraShape = camera.getShape()
        return cameraShape
    
    def getCamera(self):
        rigNode = self.getRigNode()
        return rigNode.camera.get()
    
    def setRange(self):
        ctrl = self.getCtrl()
        startFfame = ctrl.startFrame.get()
        endFrame = ctrl.endFrame.get()
        #pm.playbackOptions(min=startFfame, max=endFrame, ast=startFfame, aet=endFrame)
        pm.playbackOptions(min=startFfame, max=endFrame)
    
    def setMatch(self):
        #self.unlockNodes()
        cameraShape = self.getCameraShape()
        self.matchFilmBackToResolution(cameraShape)
        #self.lockNodes()
        
    def rename(self, newName):
        rigNode = self.getRigNode()
        #self.unlockNodes()
        allNode  = rigNode.inputs()
        cameraName = rigNode.camera.get().name()
        for node in allNode:
            new = node.name().replace(cameraName, newName)
            node.rename(new)
        
        new = rigNode.name().replace(cameraName, newName)
        rigNode.rename(new)
            
        #self.lockNodes()
        
    def setRenderable(self):
        rigNode = self.getRigNode()
        camera = rigNode.camera.get()
        cameraShape = camera.getShape()
        
        cameras = pm.ls(type='camera')
        for cam in cameras:
            cam.renderable.set(False)
    
        cameraShape.renderable.set(True)
    
    def bake(self):        
        rigNode = self.getRigNode()
        ctrl = rigNode.ctrl.get()
        camera = rigNode.camera.get()
        startFrame = ctrl.startFrame.get()
        endFrame   = ctrl.endFrame.get()
        pm.bakeResults(camera, simulation=True, t=[startFrame, endFrame])
    
    def delete(self):
        #self.unlockNodes()
        rigNode = self.getRigNode()
        conNodes = rigNode.connections()
        for node in conNodes:
            if pm.objExists(node):
                pm.delete(node) 